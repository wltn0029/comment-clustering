import axios from 'axios';
import React, { Component } from 'react';
import './UrlForm.css';

const apiKey = 'AIzaSyBhrKlcf07TRvzF5RPeKOxYSBC06TP-JUc';
const getVideoPageInfo = (videoId) => `https://www.googleapis.com/youtube/v3/videos?\
                                        part=id&key=${apiKey}&id=${videoId}`

// ref : https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
const getVideoId = videoUrl => {
  let regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
  let match = videoUrl.match(regExp);
  if (match && match[2].length === 11) {
    return match[2];
  } else {
    return undefined;
  }
}

class UrlForm extends Component {
  constructor(props) {
    super(props);
    this.inputRef = React.createRef();
    // correctInput
    // undefined : no link
    // true : right link
    // false : wrong link
    this.state = {
      correctInput : undefined
    }
    this.handleClick = this.handleClick.bind(this)
  }

  shouldComponentUpdate(nextProps, nextState) {
   if (nextState.correctInput !== this.state.correctInput) {
        return true
    }
    return false;
  }

  handleClick = (e) => {
    if (!this.inputRef.current) {
      return;
    } 
    
    if (this.inputRef.current.value.length === 0) {
      this.setState({
        correctInput: undefined
      })
      return;
    }

    const videoId = getVideoId(this.inputRef.current.value);
    if (!videoId ) {
      this.setState({
        correctInput: false
      })
      return;
    } 

    const checkUrlValid = async(videoId) => {
      const videoPageInfo = await axios.get(getVideoPageInfo(videoId));
      if (videoPageInfo.data.pageInfo.totalResults === 0) {
        this.setState({
          correctInput: false
        })
      } else {
        this.props.handleClick(videoId);
        this.setState({
          correctInput: true
        })
      }
    }

    checkUrlValid(videoId);
  }

  render() {
    const checkInputIconClass = this.state.correctInput ? 
                                  'right-input' : 
                                  this.state.correctInput === false ?
                                  'wrong-input' :
                                  'no-input'
    
    // console.log("hello")
    // console.log(this.state.videoId)
    return (
      <React.Fragment>
        <div className="center">
          <div className="title-main">
            Comment Clustering
          </div>
          <div className="blank"></div>
          <input className="input-text"
            placeholder="write youtube url"
            ref={this.inputRef}
          />
          <button className="arrange-btn" onClick={this.handleClick}>rearrange</button>
          {/* <div className={checkInputIconClass}></div> */}
        </div>
        {this.state.correctInput === false && (
          <span className = "wrong-text">
            Please insert correct url
          </span>
        )}
      </React.Fragment>
      
    );
  }
}

export default UrlForm;