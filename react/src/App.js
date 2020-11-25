import logo from './logo.svg';
import './App.css';
import React, { Component } from 'react';
import UrlForm from './components/UrlForm';

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
        <form>
          <UrlForm/>
        </form>
        </header>
      </div>
    );
  }
}

export default App;
