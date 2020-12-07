import './App.css';
import React from 'react';
import UrlForm from './components/UrlForm';
import VideoInfo from './components/VideoInfo';
import Comments from './components/Comments';
import axios from 'axios';

const fakeVideoIds = ['MXuog-hJfes','Tm9Wzzr-DUI'];
const requestUrl = 'https://143.248.144.129:8080/main';

class App extends React.Component {
  state = {
    videoId: '',
    fakeVideoId: 1,
  }

  onChangeVideoUrl = async(videoId) => {
    const serverConnection = axios.get(requestUrl);
    serverConnection
    .then( _ => this.setState({videoId}))
    .catch( _ => {
      const fakeVideoId = videoId === fakeVideoIds[0]
                          ? 0 
                          : videoId === fakeVideoIds[1] 
                          ? 1 
                          : this.state.fakeVideoId;
      this.setState({
        videoId: fakeVideoIds[fakeVideoId],
        fakeVideoId: !fakeVideoId? 1: 0
      });
    })
    
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