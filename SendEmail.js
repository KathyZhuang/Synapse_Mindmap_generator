import React, {Component} from 'react'

/**
 * A Textfield that allows the client to fetch the list of edges and draws them.
 * Also contains the buttons that the user will use to interact with the app.
 */
class SendEmail extends Component {


    /**
     * This constructor initiates the state of textBoxString as an empty string
     * It also handles user input for the canvas size which will later be validated
     * @param props: the props from EdgeListProps interface
     */
    constructor(props) {
        super(props);
        this.state = {
            emailAddress: "",
            summarizedPlain: "",
            summarized: ""
        }
    }

    componentDidMount() {
        this.getPlainSummarized();
        this.processSummarized();
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        this.getPlainSummarized();
        this.processSummarized();
    }

    getPlainSummarized = () => {
        fetch('./TPO29_Summarized.txt')
            .then(response => response.text())
            .then(data => {
                // Do something with your data
                this.state.summarizedPlain = data;
            });
    }

    processSummarized = () => {
        let lines = this.state.summarizedPlain.split("\n");
        for (let line of lines) {
            this.state.summarized += line;
        }
    }

    /**
     * Renders the email form.
     * Ensures that the path is generated before emailing it.
     */
    renderEmailForm() {
        //This is actually used
        const emailAddress = this.state.emailAddress;
        const subject = "Your Mind Map";
        if (this.state.summarized.length === 0) {
            return <>
                <div id='email-wrapper'>
                    <div id='email-header'>Send to a friend</div>
                    <input type='email' id='email-input'
                           placeholder={"friend@example.com"}
                           value={this.state.emailAddress}
                           onChange={(e) => this.setState({emailAddress: e.target.value})}/>
                    <button onClick={() => this.props.onError
                    ("You need to generate a mind map before emailing it")}>
                        <span>Send</span></button>
                </div>
            </>
        } else if (emailAddress === "") {
            return <>
                <div id='email-wrapper'>
                    <div id='email-header'>Send to a friend</div>
                    <input type='email' id='email-input'
                           placeholder={"friend@example.com"}
                           value={this.state.emailAddress}
                           onChange={(e) => this.setState({emailAddress: e.target.value})}/>
                    <button onClick={() => this.props.onError
                    ("Please enter an email address")}>
                        <span>Send</span></button>
                </div>
            </>
        } else {
            return <>
                <div id='email-wrapper'>
                    <div id='email-header'>Send to a friend</div>
                    <input type='email' id='email-input'
                           placeholder={"friend@example.com"}
                           value={this.state.emailAddress}
                           onChange={(e) => this.setState({emailAddress: e.target.value})}/>
                    <button><a
                        href={`mailto:${this.state.emailAddress}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(this.state.summarized)}`}>
                        Send</a></button>
                </div>
            </>
        }
    }

    /*href={`mailto:${this.state.emailAddress}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(this.state.summarized)}`}>
                        Send</a></button>*/

    render() {
        return (
            <div id="send-email">
                {this.renderEmailForm()}
            </div>
        );
    }
}

export default SendEmail;
