from transformers import *
from datasets import *
import torch.nn as nn
import torch.utils.data as Data
from torch.utils.data import Dataset
import torch
import os
import pickle
from textblob import TextBlob

try:
    from nsml import DATASET_PATH
    import nsml
    USE_NSML = True
except:
    USE_NSML = False

neutral_text = ["Check this video out -- President Obama at the White House Correspondents' Dinner http://bit.ly/IMXUM", 'need suggestions for a good IR filter for my canon 40D ... got some? pls DM', '@surfit: I just checked my google for my business- blip shows up as the second entry! Huh. Is that a good or ba... ? http://blip.fm/~6emhv', 'is in San Francisco at Bay to Breakers.', 'just landed at San Francisco', 'San Francisco today.  Any suggestions?', 'On my way to see Star Trek @ The Esquire.', 'Going to see star trek soon with my dad.', 'Bill Simmons in conversation with Malcolm Gladwell http://bit.ly/j9o50', 'playing with cURL and the Twitter API', 'playing with Java and the Twitter API', 'Nike owns NBA Playoffs ads w/ LeBron, Kobe, Carmelo? http://ow.ly/7Uiy  #Adidas #Billups #Howard  #Marketing #Branding', "'Next time, I'll call myself Nike'", "New blog post: Nike SB Dunk Low Premium 'White Gum' http://tr.im/lOtT", 'giving weka an app engine interface, using the bird strike data for the tests, the logo is a given.', 'Brand New Canon EOS 50D 15MP DSLR Camera Canon 17-85mm IS Lens ...: Web Technology Thread, Brand New Canon EOS 5.. http://u.mavrev.com/5a3t', "NVIDIA Names Stanford's Bill Dally Chief Scientist, VP Of Research http://bit.ly/Fvvg9", 'New blog post: Harvard Versus Stanford - Who Wins? http://bit.ly/MCoCo', 'jQuery UI 1.6 Book Review - http://cfbloggers.org/?c=30631', 'At GWT fireside chat @googleio', 'Hi there, does anyone have a great source for advice on viral marketing?... http://link.gs/YtZ8', "Here's A case study on how to use viral marketing to add over 10,000 people to your list http://snipr.com/i50oz", 'going to see the new night at the museum  movie with my family oh boy a three year old in the movies fuin', 'Just saw the new Night at the Museum movie...it was...okay...lol 7\\10', 'Going to see night at the museum 2 with tall boy', 'I saw Night at the Museum: Battle of the Swithsonian today. It was okay. Your typical [kids] Ben Stiller movie.', 'Taking Katie to see Night at the Museum.  (she picked it)', 'GM says expects announcment on sale of Hummer soon - Reuters: WDSUGM says expects announcment on sale of Hummer .. http://bit.ly/4E1Fv', "Time Warner Cable Pulls the Plug on 'The Girlfriend Experience' - (www.tinyurl.com/m595fk)", 'Rocawear Heads to China, Building 300 Stores  - http://tinyurl.com/nofet3', 'Climate focus turns to Beijing: The United Nations, the US and European governments have called on China to co-o.. http://tinyurl.com/lto92n', "myfoxdc Barrie Students Back from Trip to China: A Silver Spring high school's class trip to China has en.. http://tinyurl.com/nlhqba", 'Three China aerospace giants develop Tianjin Binhai  New Area,  22.9 B yuan invested   http://bit.ly/mMiDv', 'http://xi.gs/04FO GM CEO: China will continue to be key partner', 'RT @LATimesautos is now the time to buy a GM car? http://bit.ly/nRzlu', 'Dentist tomorrow. Have to brush well in the morning. Like I make my hair all nice before I get it cut. Why?', '@kirstiealley Pet Dentist http://www.funnyville.com/fv/pictures/dogdentures.shtml', 'NCAA Baseball Super Regional - Rams Club http://bit.ly/Ro7nx', 'just started playing Major League Baseball 2K9. http://raptr.com/H3LLGWAR', 'Cardinals baseball advance to Super Regionals. Face CS-Fullerton Friday.', 'Sony coupon code.. Expires soon.. http://www.coupondork.com/r/1796', 'waiting in line at safeway.', 'Did not realize there is a gym above Safeway!', '@XPhile1908 I have three words for you: "Safeway dot com"', 'Bout to hit safeway I gotta eat', "Jake's going to safeway!", 'Found a safeway. Picking up a few staples.', 'Safeway Super-marketing via mobile coupons http://bit.ly/ONH7w', 'Your Normal Weight (and How to Get There) ? Normal Eating Blog http://bit.ly/ZeT8O', 'Is Eating and Watching Movies....', 'eating sashimi', 'is eating  home made yema', 'eating cake', 'iPhone May Get Radio Tagging and Nike  : Recently-released iTunes version 8.2 suggests that VoiceOver functional.. http://tinyurl.com/oq5ctc', 'Launched! http://imgsearch.net  #imgsearch #ajax #jquery #webapp', 'RT @jquery: The Ultimate jQuery List - http://jquerylist.com/', 'I just extracted and open-sourced a jQuery plugin from Stormweight to highlight text with a regular expression: http://bit.ly/ybJKb', '@anna_debenham what was the php jquery hack?', 'jQuery Cheat Sheet http://www.javascripttoolbox.com/jquery/cheatsheet/', 'Beginning JavaScript and CSS Development with jQuery #javascript #css #jquery http://bit.ly/TO3e5', 'Warren Buffet on the economy http://ping.fm/Lau0p', "All-Star Basketball Classic Tuesday Features Top Talent: Chattanooga's Notre Dame High School will play host.. http://bit.ly/qltJA", 'RT Look, Available !Amazon Kindle2 &amp; Kindle DX, Get it Here: http://short.to/87ub The Top Electronic Book Reader Period, free 2 day ship ...', 'Man accosts Roger Federer during French Open http://ff.im/3HCPT', 'Investigation pending on death of Stanford CS prof / Google mentor Rajeev Motwani http://bit.ly/LwOUR tip @techmeme', "I'm going to bed. It was a successful weekend. Stanford, here I come.", 'Google Wave Developer Sandbox Account Request http://bit.ly/2NYlc', '@mattcutts have google profiles stopped showing up in searches? cant see them anymore', 'Any twitter to aprs apps yet?', '45 Pros You Should Be Following on Twitter - http://is.gd/sMbZ', "Share: Disruption...Fred Wilson's slides for his talk at Google HQ  http://bit.ly/Bo8PG", 'ok.. do nothing.. just thinking about 40D', 'RT @justindavey: RT @tweetmeme GM OnStar now instantly sends accident location coordinates to 911 | GPS Obsessed http://bit.ly/16szL1', 'breakers. in San Francisco, CA http://loopt.us/4v88Bw.t', 'Heading to San Francisco', 'How do you use the twitter API?... http://bit.ly/4VBhH', 'testing Twitter API', 'Testing Twitter API. Remote Update', 'New blog post: Nike Zoom LeBron Soldier 3 (III) - White / Black - Teal http://bit.ly/rouUS', 'New blog post: Nike Trainer 1 http://bit.ly/394bp', '#jobs #sittercity Help with taking care of sick child (East Palo Alto, CA) http://tinyurl.com/qwrr2m', '#MBA Admissions Tips Stanford GSB Deadlines and Essay Topics 2009-2010 http://tinyurl.com/pet4fd', 'Ethics and nonprofits - http://bit.ly/qsXRp  #stanford #socialentrepreneurship', 'Learning jQuery 1.3 Book Review - http://cfbloggers.org/?c=30629', 'Adobe CS4 commercial by Goodby Silverstein: http://bit.ly/1aikhF', 'Watching a programme about the life of Hitler, its only enhancing my geekiness of history.', '@pambeeslyjenna Jenna, I went to see Night At The Museum 2 today and I was so surprised to see three cast members from The Office...', 'About to watch Night at the Museum with Ryan and Stacy', 'Getting ready to go watch Night at the Museum 2.  Dum dum, you give me gum gum!', 'I think I may have a new favorite restaurant. On our way to see "Night at the Museum 2".', "UP! was sold out, so i'm seeing Night At The Museum 2. I'm __ years old.", 'Obama: Nationalization of GM to be short-term   (AP) http://tinyurl.com/md347r', 'Time Warner CEO hints at online fees for magazines      (AP) - Read from Mountain View,United States. Views 16209 http://bit.ly/UdFCH', 'Lawson to head Newedge Hong Kong http://bit.ly/xLQSD #business #china', 'Weird Piano Guitar House in China! http://u2s.me/72i8', 'Send us your GM/Chevy photos http://tinyurl.com/luzkpq', '@stevemoakler i had a dentist appt this morning and had the same conversation!', 'Check this video out -- David After Dentist http://bit.ly/47aW2', 'First dentist appointment [in years] on Wednesday possibly.', "Tom Shanahan's latest column on SDSU and its NCAA Baseball Regional appearance: http://ow.ly/axhu", 'BaseballAmerica.com: Blog: Baseball America Prospects Blog ? Blog ... http://bit.ly/EtT8a', 'Portland city politics may undo baseball park http://tinyurl.com/lpjquj', "RT @WaterSISWEB: CA Merced's water bottled by Safeway, resold at a profit: Wells are drying up across the county http://tinyurl.com/mb573s", 'dropped her broccoli walking home from safeway! ;( so depressed', "@ronjon we don't have Safeway.", 'at safeway with dad', 'Safeway with Marvin, Janelle, and Auntie Lhu', 'Safeway offering mobile coupons http://bit.ly/ONH7w', 'Phillies Driving in the Cadillac with the Top Down in Cali, Win 5-3 - http://tinyurl.com/nzcjqa', 'Saved money by opting for grocery store trip and stocking food in hotel room fridge vs. eating out every night while out of town.', 'Lounging around, eating Taco Bell and watching NCIS before work tonight. Need help staying awake.', 'eating breakfast and then school', 'still hungry after eating....', '10 tips for healthy eating ? ResultsBy Fitness Blog :: Fitness ... http://bit.ly/62gFn', 'with the boyfriend, eating a quesadilla', 'Eating dinner. Meat, chips, and risotto.', 'got a new pair of nike shoes. pics up later', 'Nike SB Blazer High "ACG" Custom - Brad Douglas - http://timesurl.at/45a448', 'Nike Air Yeezy Khaki/Pink Colorway Release - http://shar.es/bjfN', "@erickoston That looks an awful lot like one of Nike's private jets....I'm just sayin....", 'DevSnippets : jQuery Tools - Javascript UI Components for the Web... http://inblogs.org/go/hfuqt', 'all about Ajax,jquery ,css ,JavaScript and more... (many examples) http://ajaxian.com/', 'This is cold.. I was looking at google\'s chart//visualization API and found this jQuery "wrapper" for the API...  http://tinyurl.com/mq52bq', 'I spent most of my day reading a jQuery book. Now to start drinking some delirium tremens.', 'jquery Selectors http://codylindley.com/jqueryselectors/', 'How to implement a news ticker with jQuery and ten lines of code http://bit.ly/CZnFJ', "What's Buffet Doing? Warren Buffett Kicks Butt In Battle of the Boots: Posted By:Alex Crippe.. http://bit.ly/AUIzO", "I'm truly braindead.  I couldn't come up with Warren Buffet's name to save my soul", '@freitasm oh I see. I thought AT&amp;T were 900MHz WCDMA?', '@Plip Where did you read about tethering support Phil?  Just AT&amp;T or will O2 be joining in?', 'I hope the girl at work  buys my Kindle2', "Missed this insight-filled May column: One smart guy looking closely at why he's impressed with Kindle2 http://bit.ly/i0peY @wroush", '@ruby_gem My primary debit card is Visa Electron.', 'Off to the bank to get my new visa platinum card', 'has a date with bobby flay and gut fieri from food network', 'How to Track Iran with Social Media: http://bit.ly/2BoqU', 'Twitter Stock buzz: $AAPL $ES_F $SPY $SPX $PALM  (updated: 12:00 PM)', '@johncmayer is Bobby Flay joining you?', 'Ask Programming: LaTeX or InDesign?: submitted by calcio1 [link] [1 comment] http://tinyurl.com/myfmf7']

def bind_model(model, **kwargs):
    def save(filename, **kwargs):
        torch.save(model.state_dict(), f"{filename}/checkpoint.pt")
        print(f"Model saved at : {filename}/checkpoint.pt")

    def load(filename):
        checkpoint = torch.load(f"{filename}/checkpoint.pt")
        model.load_state_dict(checkpoint)
        print(f"Model named {filename} loaded")

    def infer(raw_data):  # TODO: Not complete(see below)
        data = raw_data  # TODO: need to convert raw_data to torch.Tensor object, which can be then fed into model.forward()
        model.eval()
        output = model(data)
        _, predicted = torch.max(output.data, 1)
        predicted = np.array(predicted.cpu())
        print(f"Predicted as: {predicted}")
        return predicted

    nsml.bind(save=save, load=load, infer=infer)


# for korean: https://colab.research.google.com/drive/1tIf0Ugdqg4qT7gcxia3tL7und64Rv1dP

class TwitterDataset(Dataset):
    def __init__(self, dataset):
        self.input_ids = dataset['input_ids']
        self.attn_mask = dataset['attention_mask']
        self.ttids = dataset['token_type_ids']
        self.label_list = dataset['sentiment']
        self.label_list = self.label_list // 2 # 0, 4 -> 0, 1 labels are 0,1

    def __len__(self):
        return len(self.label_list)

    def __getitem__(self, idx):
        inputs = {'input_ids': self.input_ids[idx], 'attention_mask': self.attn_mask[idx], 'token_type_ids': self.ttids[idx]}
        return inputs, self.label_list[idx]

class Trainer:
    def __init__(self, use_nsml):
        self.args = {'epoch': 10, 'learning_rate': 5e-05}
        self.step = 0
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.nsml = use_nsml
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.model, self.optimizer, self.scheduler, self.criterion, self.train_data, self.test_data, self.train_loader,\
            self.test_loader, self.data, self.datasets = None, None, None, None, None, None, None, None, None, None
        #self.configure_dataset()
        #self.configure_model(len(self.train_loader))
        path = '/Users/user/Desktop/coding/comment-clustering-model/KR62640_None_3528/twitter-rand-5/model/checkpoint.pt'
        self.load_and_eval(path)
        self.train()

    def convert_cuda(self, inputs, targets):
        for key in inputs.keys():
            inputs[key] = inputs[key].to(self.device)
        targets = targets.to(self.device)
        return inputs, targets

    def configure_model(self, loader_length):
        config = BertConfig.from_pretrained('bert-base-uncased')
        config.num_labels = 3
        self.model = BertForSequenceClassification.from_pretrained("bert-base-uncased", config=config).to(self.device)
        self.model = nn.DataParallel(self.model)
        if self.nsml:
            bind_model(self.model)
        # TODO: add n_labels
        no_decay = ['bias', 'LayerNorm.weight']
        optimizer_grouped_parameters = [
            {
                "params": [p for n, p in self.model.named_parameters() if not any(nd in n for nd in no_decay)],
                "weight_decay": 1e-4  # 10^-4 good at mixup paper
            },
            {
                "params": [p for n, p in self.model.named_parameters() if any(nd in n for nd in no_decay)],
                "weight_decay": 0
            },
        ]
        self.optimizer = AdamW(optimizer_grouped_parameters, lr=self.args['learning_rate'], eps=1e-8)
        self.scheduler = get_linear_schedule_with_warmup(self.optimizer,
                                                         num_warmup_steps=loader_length * self.args['epoch'] // 10,
                                                         num_training_steps=loader_length * self.args['epoch'])
        self.criterion = nn.CrossEntropyLoss()

    def configure_dataset(self):
        def tokenize(example):
            return self.tokenizer(example['text'], padding='max_length', max_length=256, truncation=True)
        if not self.nsml and os.path.exists('data.pickle'):
            with open('data.pickle', 'rb') as f:
                self.datasets = pickle.load(f)
        else:
            self.data = load_dataset('sentiment140')
            self.datasets = self.data.map(tokenize, batched=True, load_from_cache_file=True)
            with open('data.pickle', 'wb') as f:
                pickle.dump(self.datasets, f)
        self.datasets.set_format(type='torch', columns=['input_ids', 'token_type_ids', 'attention_mask', 'sentiment'])
        self.train_data = TwitterDataset(self.datasets['train'])
        self.test_data = TwitterDataset(self.datasets['test'])
        self.train_loader = Data.DataLoader(dataset=self.train_data, batch_size=128, shuffle=True)
        self.test_loader = Data.DataLoader(dataset=self.test_data, batch_size=128, shuffle=True)
        print(f"Configured train_loader of {len(self.train_loader)}, test_loader of {len(self.test_loader)}")

    def train(self):
        best_acc = 0
        self.model.train()
        for epoch in range(self.args['epoch']):
            for batch_idx, data in enumerate(self.train_loader):
                self.step += 1
                inputs, targets = data
                inputs, targets = self.convert_cuda(inputs, targets)
                outputs = self.model(**inputs)[0]
                loss = self.criterion(outputs, targets)
                #print(f"batch: {batch_idx}, loss: {loss}")
                if self.nsml:
                    nsml.report(step=self.step, scope=locals(), summary=True, train__epoch=epoch, train__loss=loss.item())
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                self.scheduler.step()
            """
            correct = 0
            total_sample = 0
            loss_total = 0
            for data in self.test_loader:
                inputs, targets = data
                inputs, targets = self.convert_cuda(inputs, targets)
                outputs = self.model(**inputs)[0]
                loss = self.criterion(outputs, targets)
                predicted = torch.argmax(outputs, dim=1)
                correct += (predicted == targets).sum()
                loss_total += loss.item() * len(inputs['input_ids'])
                total_sample += inputs['input_ids'].shape[0]

            acc_total = float(correct) / total_sample
            loss_total = float(loss_total) / total_sample
            if self.nsml:
                nsml.report(step=epoch, scope=locals(), summary=True, test__loss=loss_total, test_acc=acc_total)
            print(f"epoch: {epoch}, test loss: {loss_total}, test acc: {acc_total}")
            """
            acc_total = 1
            best_acc = 0
            if acc_total > best_acc:
                print("Saving checkpoint")
                if self.nsml:
                    nsml.save(checkpoint=f"twitter-rand-3-{epoch}")
                else:
                    torch.save(self.model.state_dict(), f"twitter-best-{epoch}.pt")
                print("saved")

    def load_and_eval(self, path):
        config = BertConfig.from_pretrained('bert-base-uncased')
        config.num_labels = 2
        self.model = BertForSequenceClassification.from_pretrained("bert-base-uncased", config=config).to(self.device)
        self.model = nn.DataParallel(self.model)
        checkpoint = torch.load(path, map_location=torch.device('cpu'))
        #state_dict = checkpoint['state_dict']
        """
        for name, param in model.state_dict.items():
            if name == "module.bert.embeddings.position_ids":
                continue
            else:
        """
        self.model.load_state_dict(checkpoint, strict=False)
        def test(text):
            inputs = self.tokenizer(text, padding='max_length', max_length=256, truncation=True, return_tensors='pt')
            output = self.model(**inputs)[0]
            predicted = output.argmax().item()
            if predicted == 1:
                return f"{[output[0][0].item(), output[0][1].item()]}, positive"
            elif predicted == 0:
                return f"{[output[0][0].item(), output[0][1].item()]}, negative"

        for t in neutral_text:
            print(f"\n\ninput   | {t}")
            print(f"model   | {test(t)}")
            print(f"library | {TextBlob(t).sentiment.polarity}")

aa = Trainer(USE_NSML)
