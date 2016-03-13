/**
    Copyright 2014-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

        http://aws.amazon.com/apache2.0/

    or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/

/**
 * This simple sample has no external dependencies or session management, and shows the most basic
 * example of how to create a Lambda function for handling Alexa Skill requests.
 *
 * Examples:
 * One-shot model:
 *  User: "Alexa, tell Greeter to say hello"
 *  Alexa: "Hello World!"
 */

/**
 * App ID for the skill
 */
var APP_ID = "amzn1.echo-sdk-ams.app.84bace95-e347-40e9-b43c-b7934c7ad60e";


/**
 * The AlexaSkill prototype and helper functions
 */
var AlexaSkill = require('./AlexaSkill');
var Firebase = require("./node_modules/firebase/lib/firebase-node");
var rootRef = new Firebase('https://hackalexa.firebaseio.com');
var childRefTest = rootRef.child('test');
var childRefFace = rootRef.child('face');

/**
 * HelloWorld is a child of AlexaSkill.
 * To read more about inheritance in JavaScript, see the link below.
 *
 * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Introduction_to_Object-Oriented_JavaScript#Inheritance
 */
var HelloWorld = function () {
    AlexaSkill.call(this, APP_ID);
};

// Extend AlexaSkill
HelloWorld.prototype = Object.create(AlexaSkill.prototype);
HelloWorld.prototype.constructor = HelloWorld;

HelloWorld.prototype.eventHandlers.onSessionStarted = function (sessionStartedRequest, session) {
    console.log("HelloWorld onSessionStarted requestId: " + sessionStartedRequest.requestId
        + ", sessionId: " + session.sessionId);
    // any initialization logic goes here
};

HelloWorld.prototype.eventHandlers.onLaunch = function (launchRequest, session, response) {
    console.log("HelloWorld onLaunch requestId: " + launchRequest.requestId + ", sessionId: " + session.sessionId);
    var speechOutput = "Welcome, you can say I am going out or who came by";
    var repromptText = "you can say I am going out or who came by";
    response.ask(speechOutput, repromptText);
};

HelloWorld.prototype.eventHandlers.onSessionEnded = function (sessionEndedRequest, session) {
    console.log("HelloWorld onSessionEnded requestId: " + sessionEndedRequest.requestId
        + ", sessionId: " + session.sessionId);
    // any cleanup logic goes here

        // // reset the DB
        // childRefFace.on("value", function(snapshot) {
        //     if (snapshot.val().playVideo === false) {
        //        childRefFace.update({
        //            playVideo:false
        //            numOfVisitors:0
        //        });
        //     }
        // }, function (errorObject) {
        //     console.log("The read failed: " + errorObject.code);
        // });

    //childRef.update({
    //    isAsked2: false
    //});
};

HelloWorld.prototype.intentHandlers = {
    // register custom intent handlers
    "GetFace": function (intent, session, response) {
        var numOfVisitors = null;
        var speechOutput;
        childRefFace.on("value", function(snapshot) {
            numOfVisitors = snapshot.val().numOfVisitors;
            // console.log("Input type: " + typeof colorSlot + ", Database type: " + typeof color);
            if (numOfVisitors === 0) {
                 speechOutput={
                    speech: "Unfortunately, there were no visitors",
                    type: AlexaSkill.speechOutputType.PLAIN_TEXT
                };
            } else {
                speechOutput={
                    speech: "There were " + numOfVisitors + " visitors, do you want me to show you the visitors? ",
                    type: AlexaSkill.speechOutputType.PLAIN_TEXT
                };
            }
            response.ask(speechOutput);
        }, function (errorObject) {
            console.log("The read failed: " + errorObject.code);
        });
    },
    "IsOut": function (intent, session, response) {
        var speechOutput;
        childRefFace.on("value", function(snapshot) {
            console.log(snapshot.val());
            childRefFace.update({
                "isOut": true // should be false by default
            });
            speechOutput={
                    speech: "Ok, I will keep an eye on our house",
                    type: AlexaSkill.speechOutputType.PLAIN_TEXT
                };
            childRefFace.off("value");
            response.ask(speechOutput);
        }, function (errorObject) {
            console.log("The read failed: " + errorObject.code);
        });
    },
    "IsBack": function (intent, session, response) {
        var numOfVisitors;
        var speechOutput;
        childRefFace.on("value", function(snapshot) {
            console.log(snapshot.val());
            numOfVisitors = snapshot.val().numOfVisitors;
            childRefFace.update({
                "isOut": false
            });
            if (numOfVisitors === 0) {
                 speechOutput={
                    speech: "Welcome back, nobody visited you when you were out",
                    type: AlexaSkill.speechOutputType.PLAIN_TEXT
                };
            } else {
                speechOutput={
                    speech: "Welcome back, there were " + numOfVisitors + " visitors, do you want me to show you the visitors? ",
                    type: AlexaSkill.speechOutputType.PLAIN_TEXT
                };
            }
            childRefFace.off("value");
            response.ask(speechOutput);
        }, function (errorObject) {
            console.log("The read failed: " + errorObject.code);
        });
    },
    "ShowVisitors": function (intent, session, response) {
        var speechOutput;
        var num;
        var numOfVisitors;
        childRefFace.on("value", function(snapshot) {
            console.log(snapshot.val());
            num = snapshot.val().playIndex;
            numOfVisitors = snapshot.val().numOfVisitors;
            childRefFace.update({
                "playVideo":true
            });
            if (num<=numOfVisitors) {
                speechOutput={
                    speech: "Here is the video",
                    type: AlexaSkill.speechOutputType.PLAIN_TEXT
                };
                childRefFace.off("value");
                response.ask(speechOutput);
            }else{
                speechOutput={
                    speech: "No more videos, start from the first one",
                    type: AlexaSkill.speechOutputType.PLAIN_TEXT
                };
                childRefFace.off("value");
                response.ask(speechOutput);
                childRefFace.update({
                // "numOfVisitors":0,
                    "playIndex":1
                });
            }
            // childRefFace.off("value");
            // response.ask(speechOutput);
        }, function (errorObject) {
            console.log("The read failed: " + errorObject.code);
        });

    },
    "AMAZON.HelpIntent": function (intent, session, response) {
        response.ask("What color is it", "What color is it");
    }
};

// Create the handler that responds to the Alexa Request.
exports.handler = function (event, context) {
    // Create an instance of the HelloWorld skill.
    var helloWorld = new HelloWorld();
    helloWorld.execute(event, context);
};

