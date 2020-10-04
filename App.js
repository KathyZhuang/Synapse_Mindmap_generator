
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
import PrintFile from "./PrintFile";
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
            summarized: "",
            errorMessage: undefined
        };
    }

    /**
     * Sets the state of the error when error occurs given a error message
     * @param errorMessage
     */
    onError = (errorMessage) => {
        this.setState({
            errorMessage: errorMessage
        });
    }


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
                <PrintFile/>
                <SendEmail onError={this.onError}/>
            </div>
        );
    }
}

export default App;
