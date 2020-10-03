
/*
 * Copyright ©2019 Dan Grossman.  All rights reserved.  Permission is
 * hereby granted to students registered for University of Washington
 * CSE 331 for use solely during Autumn Quarter 2019 for purposes of
 * the course.  No other use, copying, distribution, or modification
 * is permitted without prior written consent. Copyrights for
 * third-party components of this work must be honored.  Instructors
 * interested in reusing these course materials should contact the
 * author.
 */

import React, {Component} from 'react';
import EdgeList from "./EdgeList";
import Grid from "./Grid";
import GridSizePicker from "./GridSizePicker";

// Allows us to write CSS styles inside App.css, any any styles will apply to all components inside <App />
/*<GridSizePicker value={this.state.gridSize} onChange={this.updateGridSize}/>
                <Grid size={this.state.gridSize} width={canvas_size} height={canvas_size} alertSize={this.state.checkSize}
                      edgeArray={this.state.parsedEdges}/>
                <EdgeList value={this.state.edges} gridSize={this.state.gridSize} onChange={this.updateEdgeText}
                          updateEdge={this.updateEdgeList}/>

 */
import "./App.css";
import SendEmail from "./SendEmail";

class App extends Component {

    constructor(props) {
        super(props);

        //this.processLineByLine();
        this.state = {
            gridSize: 4,  // The number of points in the grid
            edges: "",
            checkSize: false,
            parsedEdges: [],
            summarized: ""
        };

        /* File System Object */
        fetch('./TPO29_Original.txt')
            .then(response => response.text())
            .then(data => {
                // Do something with your data
                this.printByLine(data);
                //document.write(data);
                //this.state.originalText = data;
            });

        fetch('./TPO29_Summarized.txt')
            .then(response => response.text())
            .then(data => {
                // Do something with your data
                this.printSummarizedByLine(data);
                //document.write(data);
                //this.state.originalText = data;
            });
    }

    printByLine = (text) => {
        this.state.summarized = text;
        let lines = text.split(".");
        for (let line of lines) {
            document.write(line + ".");
            document.write("<br>");
        }
    }

    printSummarizedByLine = (text) => {
        let lines = text.split("\n");
        for (let line of lines) {
            document.write(line.substring(0,line.length - 3));
            document.write("<br>");
        }
    }

    async processLineByLine() {
        const fs = require('fs');
        const readline = require('readline');
        const fileStream = fs.createReadStream('./TPO29_Original.txt');

        var TxtFile = function(ClassName)
        {
            this.ClassName = ClassName;
            this.Fso = null;
            this.Delay = 10000;//多长时间读bai取du一次
            this.ReadLine = 0;//初始化，从第几行开始读取
            this.RowCount = 1;//文本的zhi总行数
            this.TxtContent = null;//文本的内容,数组
            this.ForReading = 1;//只读
        }

        TxtFile.prototype.CreateObject = function()
        {
            if(this.Fso == null)
            {
                //this.Fso = new ActiveXObject("Scripting.FileSystemObject");
            }
        }
        TxtFile.prototype.OpenFile = function(TxtFilePath)
        {
            this.CreateObject();
            try
            {
                var f = this.Fso.OpenTextFile(TxtFilePath,this.ForReading);
            }
            catch (e)
            {
                alert("文件不存在");
                return;
            }
            if(f.AtEndOfLine)
            {
                alert('空文件!');
                this.RowCount = 1;
                this.TxtContent = [""];
            }
            else
            {
                this.TxtContent = f.ReadAll().split("\r\n");
                this.RowCount = this.TxtContent.length;
            }
            this.ToAlertFileConten();
        }
        TxtFile.prototype.ToAlertFileConten = function()
        {
            if(this.ReadLine < this.RowCount )
            {
                alert(this.TxtContent[this.ReadLine]);
            }
            if(this.ReadLine ==this.RowCount - 1)
            {
                alert("文件读取完毕。");
            }
            else
            {
                this.ReadLine++;
                window.setTimeout(""+ this.ClassName +".ToAlertFileConten();",this.Delay);
            }
        }
        var MyTxtFile = new TxtFile("MyTxtFile");
        MyTxtFile.OpenFile("./TPO29_Original.txt");

        const rl = readline.createInterface({
            input: fileStream,
            crlfDelay: Infinity
        });
        // Note: we use the crlfDelay option to recognize all instances of CR LF
        // ('\r\n') in input.txt as a single line break.

        for await (const line of rl) {
            // Each line in input.txt will be successively available here as `line`.
            console.log(`Line from file: ${line}`);
        }
    }

    getText = () => {
        fetch('./TPO29_Original.txt')
            .then(response => response.text())
            .then(data => {
                // Do something with your data
                document.write(data);
            });
    }
    updateGridSize = (validatedSize) => {
        // Every event handler with JS can optionally take a single parameter that
        // is an "event" object - contains information about an event. For mouse clicks,
        // it'll tell you thinks like what x/y coordinates the click was at. For text
        // box updates, it'll tell you the new contents of the text box, like we're using
        // below:
       this.setState({
           checkSize: true,
           gridSize: validatedSize
       });
    };

    updateEdgeText = (event) => {
        this.setState({
            checkSize: false,
            edges: event.target.value
        });
    };

    updateEdgeList = (edgeArray) => {
        this.setState({
            checkSize: true,
            parsedEdges: edgeArray});
    };


    render() {
        const canvas_size = 500;
        /* File System Object */
        //document.write(this.state.originalText);
        //document.write(this.state.originalText);
        //document.write(" ");
        //document.write(this.state.mindMap);
        return (
            <div>
                <p id="app-title">Get the Mind Map!</p>
                <SendEmail text = {this.state.summarized}/>
            </div>
        );
    }
}

export default App;
