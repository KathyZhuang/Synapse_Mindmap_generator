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
            emailAddress: ""
        }
    }

    /**
     * Renders the email form.
     * Ensures that the path is generated before emailing it.
     */
    renderEmailForm() {
        //This is actually used
        const emailAddress = this.state.emailAddress;
        const subject = "Your route details";
        let emailBody = this.props.text;

        if (emailAddress === "") {
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
                        href={`mailto:${this.state.emailAddress}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(emailBody)}`}>
                        Send</a></button>
                </div>
            </>
        }
    }

    render() {
        return (
            <div id="send-email">
                {this.renderEmailForm()}
            </div>
        );
    }
}

export default SendEmail;
