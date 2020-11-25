import React, { Component } from 'react';
import axios from 'axios';

//api key for youtube comment api
const apiKey = 'AIzaSyBhrKlcf07TRvzF5RPeKOxYSBC06TP-JUc';
const getUrl = videoId => `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&key=${apiKey}\
                              &videoId=${videoId}&maxResults=100`

// ref : https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
const getVideoId = videoUrl => {
  var regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
  var match = videoUrl.match(regExp);
  if (match && match[2].length == 11) {
    return match[2];
  } else {
    return undefined;
  }
}

class UrlForm extends Component {
  state = {
    url: ''
  }
  handleChange = (e) => {
    this.setState({
      url: e.target.value
    });
  }
  onClick = (e) => {
    e.preventDefault();

    const apiCall = async () => { 
      const response = await axios.get(getUrl(getVideoId(this.state.url))); 
      console.log(response); 
    };

    apiCall();

  }
  render() {
    return (
      <div className="url-form">
        <input
          placeholder="write youtube url"
          onChange={this.handleChange}
        />
        <button onClick={this.onClick}>rearrange</button>
      </div>
    );
  }
}

export default UrlForm;