import React, { Component } from 'react';
import axios from 'axios';

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
        const videoInfo = await axios.get(getVideoInfo(videoId));
        const videoInfoData = videoInfo.data.items[0].snippet;
        const channelId = videoInfoData.channelId;
        const videoTitle = videoInfoData.title;
        const description = videoInfoData.description;
        const videoThumbnail = videoInfoData.thumbnails.default.url;

        const channelInfo = await axios.get(getChannelInfo(channelId));
        const channelImg = channelInfo.data.items[0].snippet.thumbnails.default.url;
        
        this.setState({videoTitle, videoThumbnail, description, channelImg});
    }

    render() {
        const {videoTitle, videoThumbnail, description, channelImg} = this.state;
        console.log('render')
        return (
            <div  className="video-info">
                {videoThumbnail && (<img src={videoThumbnail}/>)}
                {videoTitle && (<div>{videoTitle}</div>)}
                {description && (<div>{description}</div>)}
                {channelImg && (<img src={channelImg}/>)}
            </div>
           
        );
    }
}

export default VideoInfo;