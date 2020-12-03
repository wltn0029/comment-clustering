import React, { Component } from 'react';
import axios from 'axios';
import CommentThread from './CommentThread';
import { Buffer } from 'buffer'
import CommentThreadCss from './CommentThread.css';

const apiKey = 'AIzaSyBhrKlcf07TRvzF5RPeKOxYSBC06TP-JUc';
const getCommentThreads = videoId => `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&key=${apiKey}\
                                        &videoId=${videoId}&maxResults=100`;
const requestUrl = 'http://143.248.144.129:8080/main';
class Comments extends Component {
    constructor(props) {
        super(props);
        this.state = {
            neg : [],
            pos : [],
            neu : [],
            selectedCategory: ''
        }
    }

    shouldComponentUpdate(nextProps, nextState) {
        if (nextProps.videoId !== this.props.videoId) {
            this.analyzeComments(nextProps.videoId);
            return true;
        } else if (nextState.neg !== this.state.neg ||
                    nextState.pos !== this.state.pos ||
                    nextState.neu !== this.state.neu || 
                    nextState.selectedCategory !== this.state.selectedCategory) {
            return true
        }
        return false;
    }

    analyzeComments = async(videoId) => {
        if (!videoId) {
            return;
        }
        const comments = await axios.get(getCommentThreads(videoId));
        const convertedComments = comments.data.items.map(comment => {
            const id = comment.snippet.topLevelComment.id
            const {authorDisplayName, authorProfileImageUrl, textOriginal} = 
                {...comment.snippet.topLevelComment.snippet}
            return {id, authorDisplayName, authorProfileImageUrl, textOriginal}
        })
        
        // Request : send comments to server to get sentimental results
        // method : POST
        // body : { rawData : convertedComments }
        // response : {pos : commentsList, neg : commentList, neu : commentList }
        const postBody = {
            rawData : convertedComments 
        };
        const requestMetadata = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=utf-8'
                
            },
            body: JSON.stringify(postBody)
        };
        
        console.log(requestMetadata)
        fetch(requestUrl, requestMetadata)
            .then(res => {
                //todo : fetch server's response and render it  
            })

        this.setState({
            pos: convertedComments
        })
    }

    // category 
    // pos : expand positive comments
    // neu : expand neutral comments
    // neg : expand negative comments
    // '' : nothing to expand 
    isSelected = (category) => {
        if (this.state.selectedCategory === '') {
            return false;
        } else if (this.state.selectedCategory === category) {
            return true;
        } else {
            return undefined;
        }
    }

    expandCommentThreads = (category) => {
        console.log('expandcommentthread', category)
        this.setState({selectedCategory: category})
    }

    render() {
        const {pos, neg, neu} = this.state;
        return (
            <div className="comments">
                {(pos.length !==0 || neg.length !== 0 || neu.length !== 0) && (
                    <div>
                        <CommentThread category="pos" comments={this.state.pos}
                            expand={this.isSelected("pos")} handleClick={this.expandCommentThreads}/>
                        <CommentThread category="neu" comments={this.state.neu} 
                            expand={this.isSelected("neu")} handleClick={this.expandCommentThreads}/>
                        <CommentThread category="neg" comments={this.state.neg} 
                            expand={this.isSelected("neg")} handleClick={this.expandCommentThreads}/>
                    </div>
                ) }
            </div>
        );
    }
}

export default Comments;