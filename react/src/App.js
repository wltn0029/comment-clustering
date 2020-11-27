import './App.css';
import React from 'react';
import UrlForm from './components/UrlForm';
import VideoInfo from './components/VideoInfo';
import Comments from './components/Comments';

class App extends React.Component {
  state = {
    videoId: '',
  }

  onChangeVideoUrl = (videoId) => this.setState({videoId})

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
