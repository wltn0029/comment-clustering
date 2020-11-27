import React, { Component } from 'react';
import classNames from 'classnames';

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
        console.log(`expand for ${this.props.category} ${this.props.expand}`);
        return (
            expand !== undefined && (
                <div  className={classNames('comment-thread', {expand : expand})}>
                    <button onClick={this.handleClick}/>
                    {commentThread.map(comment => (
                        <Comment 
                            key={comment.id}
                            authorDisplayName={comment.authorDisplayName}
                            authorProfileImageUrl={comment.authorProfileImageUrl}
                            textOriginal={comment.textOriginal}/>
                    ))}
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
                <img src={authorProfileImageUrl}/>
                <span>{authorDisplayName}</span>
                <span>{textOriginal}</span>
            </React.Fragment>
        )
    }
}

export default CommentThread;