import React, { Component } from 'react';
// import classNames from 'classnames';
import './CommentThread.css';

class CommentThread extends Component { 
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick = (e) => {
        const {expand, category} = this.props;
        if (expand) {
            this.props.handleClick('');
        } else {
            this.props.handleClick(category);
        }
    }

    render() {
        // expand (true, false, undefined)
        // true: expand
        // false : show top comment
        // undefined : nothing to show
        const {expand, comments} = this.props;
        const commentThread = expand? comments : comments.slice(0,1);
        const isShowMore = expand? 'Close' : 'Show More';
        const categoryName = this.props.category === "pos" ? "POSITIVE" : this.props.category === "neu" ? "NEUTRALITY" : "NEGATIVE"

        return (
            expand !== undefined && (
                <div>
                    <div className="category">
                        <span className="category-name">{categoryName}</span>
                        <button className='thread-btn' onClick={this.handleClick}>{isShowMore}</button>
                    </div>
                    <div>
                    {commentThread.map(comment => (
                        <Comment 
                            key={comment.id}
                            authorDisplayName={comment.authorDisplayName}
                            authorProfileImageUrl={comment.authorProfileImageUrl}
                            textOriginal={comment.textOriginal}/>
                    ))}
                    </div>
                </div>
            )
        );
    }
}

class Comment extends Component {
    render() {
        const {authorDisplayName, authorProfileImageUrl, textOriginal} = this.props;
        return(
            <React.Fragment>
                <div className="profile">
                    {/* <img className='profile-image' src={authorProfileImageUrl}/> */}
                    <span className='user-name'>{authorDisplayName}</span>
                    <span> : </span>
                    <span className='comment-text'>{textOriginal}</span>
                </div>
            </React.Fragment>
        )
    }
}

export default CommentThread;