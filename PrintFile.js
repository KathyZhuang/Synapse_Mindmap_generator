/* Constructs a drop-down menu that allows users to choose from all campus buildings */

import React, {Component} from 'react';

class PrintFile extends Component {

    constructor(props) {
        super(props);
        this.state = {
            backgroundImage: null,
            y: null
        };
        this.canvas = React.createRef();
    }

    componentDidMount() {
        let canvas = this.canvas.current;
        canvas.width = 1000;
        canvas.height = 1300;

        this.printOriginal();
    }

    componentDidUpdate() {
        this.printOriginal();
    }

    printOriginal = () => {
        /* File System Object */
        fetch('./TPO29_Original.txt')
            .then(response => response.text())
            .then(data => {
                this.printByLine(data);
            });
    }

    printSummarized = () => {
        fetch('./TPO29_Summarized.txt')
            .then(response => response.text())
            .then(data => {
                // Do something with your data
                this.printSummarizedByLine(data);
            });
    }

    printByLine = (text) => {
        let canvas = this.canvas.current;
        let ctx = canvas.getContext("2d");
        ctx.font = "30px Arial";
        let lines = text.split(".");
        let x = 10;
        let y = 50;
        ctx.fillText("Original Text", x, y);
        y = y + 30;
        ctx.font = "10px Arial";
        for (let line of lines) {
            ctx.fillText(line + ".", x, y);
            y += 10;
        }
        this.state.y = y;
    }

    printSummarizedByLine = (text) => {
        let canvas = this.canvas.current;
        let ctx = canvas.getContext("2d");
        ctx.font = "30px Arial";
        let lines = text.split("\n");

        let x = 10;
        let y = this.state.y;
        y += 30;
        ctx.fillText("Summarized Text", x, y);
        y += 30;
        ctx.font = "15px Arial";
        for (let line of lines) {
            line = line.substring(0, line.length - 3);
            ctx.fillText(line, x, y);
            y += 15;
        }
    }

    render() {
        return (
            <div>
                <canvas ref={this.canvas}/>
                <button onClick={this.printSummarized}>Generate Mind Map</button>
            </div>
        );
    }
}

export default PrintFile;