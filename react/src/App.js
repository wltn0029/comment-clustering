import './App.css';
import React from 'react';
import UrlForm from './components/UrlForm';
import VideoInfo from './components/VideoInfo';
import Comments from './components/Comments';

//youtube comment api
const apiKey = 'AIzaSyBhrKlcf07TRvzF5RPeKOxYSBC06TP-JUc';
const getCommentThreads = videoId => `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&key=${apiKey}\
                              &videoId=${videoId}&maxResults=100`
const getVideoInfo = videoId => `https://www.googleapis.com/youtube/v3/videos?part=snippet&key=${apiKey}\
                              &videoId=${videoId}`
const getChannelImgUrl = channelId => `https://www.googleapis.com/youtube/v3/channels?part=snippet&key=${apiKey}\
                              &id=${channelId}`

// ref : https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
const getVideoId = videoUrl => {
  let regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
  let match = videoUrl.match(regExp);
  if (match && match[2].length == 11) {
    return match[2];
  } else {
    return undefined;
  }
}
class App extends React.Component {
  state = {
    videoId: '',
  }

  onChangeVideoUrl = (videoUrl) => {
    if (!videoUrl) {
      return;
    }
    this.setState({videoId: getVideoId(videoUrl)})
  }

  render() {
    return (
      <div className="App">
          <UrlForm handleClick={this.onChangeVideoUrl}/>
          <VideoInfo videoId={this.state.videoId}/>
          <Comments videoId={this.state.videoId}/>
      </div>
    );
  }
}

export default App;
