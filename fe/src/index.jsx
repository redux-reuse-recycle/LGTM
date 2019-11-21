import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import path from 'path';
import {
    HashRouter as Router,
} from "react-router-dom";
import dotenv from 'dotenv';

dotenv.config({ path: path.resolve(__dirname, '../.env') });

ReactDOM.render(
    <Router>
        <App />
    </Router>
, document.getElementById('root'));
