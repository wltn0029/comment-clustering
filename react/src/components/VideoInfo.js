import React, { Component } from 'react';
import axios from 'axios';
import './VideoInfo.css';

const apiKey = 'AIzaSyBhrKlcf07TRvzF5RPeKOxYSBC06TP-JUc';
const getVideoInfo = videoId => `https://www.googleapis.com/youtube/v3/videos?part=snippet&key=${apiKey}\
                              &id=${videoId}`
const getChannelInfo = channelId => `https://www.googleapis.com/youtube/v3/channels?part=snippet&key=${apiKey}\
                              &id=${channelId}`

class VideoInfo extends Component {
    constructor(props) {
        super(props);
        this.state = {
            videoTitle : '',
            description: '',
            videoThumbnail: '',
            channelImg : ''
        }
    }

    shouldComponentUpdate(nextProps, nextState) {
        if (nextProps.videoId !== this.props.videoId) {
            this.updateVideoInfo(nextProps.videoId);
            return true;
        } else if (nextState.videoTitle !== this.state.videoTitle ||
                    nextState.videoThumbnail !== this.state.videoThumbnail ||
                    nextState.description !== this.state.default ||
                    nextState.channelImg !== this.state.channelImg) {
            return true
        }
        return false;
    }

    updateVideoInfo = async(videoId) => {
        if (!videoId) {
            return;
        }
        console.log('videoId');
        const videoInfo = await axios.get(getVideoInfo(videoId));
        const {channelId, title, description, thumbnails}  = {...videoInfo.data.items[0].snippet};
        const videoThumbnail = thumbnails.default.url;

        const channelInfo = await axios.get(getChannelInfo(channelId));
        const channelImg = channelInfo.data.items[0].snippet.thumbnails.default.url;
        
        this.setState({videoTitle: title, videoThumbnail, description, channelImg});
    }

    render() {
        const {videoTitle, videoThumbnail, description, channelImg} = this.state;
        // console.log('render')
        return (
            <div className="video-info">
                <div className="video-title-info">
                    {/* {videoThumbnail && (<img className="video-thumbnail" src={videoThumbnail}/>)} */}
                    {videoTitle && (<text className="video-title">{videoTitle}</text>)}
                </div>
                <div>
                    {/* {channelImg && (<img className="video-img" src={channelImg}/>)} */}
                    {description && (<div className="video-description">{description}</div>)}
                </div>
            </div>
           
        );
    }
}

export default VideoInfo;