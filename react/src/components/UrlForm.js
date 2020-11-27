import React, { Component } from 'react';
import axios from 'axios';


class UrlForm extends Component {
  constructor(props) {
    super(props);
    this.inputRef = React.createRef();
    this.handleClick = this.handleClick.bind(this)
  }

  handleClick = (e) => {
    console.log(this.inputRef.current.value);
    if (!this.inputRef.current) {
      return;
    }
    this.props.handleClick(this.inputRef.current.value)
  }

  render() {
    return (
      <div className="url-form">
        <input
          placeholder="write youtube url"
          ref={this.inputRef}
        />
        <button onClick={this.handleClick}>rearrange</button>
      </div>
    );
  }
}

export default UrlForm;