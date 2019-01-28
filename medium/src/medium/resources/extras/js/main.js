// Hive Solutions Development
// Copyright (c) 2008-2019 Hive Solutions Lda.
//
// This file is part of Hive Solutions Development.
//
// Hive Solutions Development is confidential and property of Hive Solutions Lda.,
// its usage is constrained by the terms of the Hive Solutions
// Confidential Usage License.
//
// Hive Solutions Development should not be distributed under any circumstances,
// violation of this may imply legal action.
//
// If you have any questions regarding the terms of this license please
// refer to <http://www.hive.pt/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2008-2019 Hive Solutions Lda.
// __license__   = Hive Solutions Confidential Usage License (HSCUL)

jQuery(document).ready(function() {
    // retrieves the body element
    var _body = jQuery("body");

    // retrieves the commits author week field
    var fieldCommitsAuthorWeek = jQuery("#field-commits_author_week");

    // starts the scheduler
    _body.scheduler();

    // starts the ticker
    _body.ticker();

    // starts the time
    _body.time();

    // starts the communication
    _body.communication("default", {
        url: "communication",
        channels: ["public"],
        timeout: 500,
        callbacks: [messageProcessor]
    });

    // registers for the stream connected event
    _body.bind("stream_connected", function() {
        // hides the error message
        _body.error("hide");
    });

    // registers for the stream disconnected event
    _body.bind("stream_disconnected", function() {
        // shows the error message
        _body.error("show", {
            "message": "Disconnected from server"
        });
    });

    // registers for the stream error event
    _body.bind("stream_error", function() {
        // shows the error message
        _body.error("show", {
            "message": "Error communicating with server"
        });
    });

    // registers for the set field event
    _body.bind("set_field_commits_author_week",
        function(event, key, value) {
            // retrieves the commit chart element
            var commitChart = jQuery("#commit-chart");

            // draws the commit chart
            commitChart.weekchart({
                value: value
            });
        });

    // updates the field commits author chart in case the field
    // is already set
    fieldCommitsAuthorWeek.each(function(index, element) {
        // retrieves the element
        var element = jQuery(this);

        // retrieves the element contents
        var elementContents = element.html();

        // retrieves the commit chart element
        var commitChart = jQuery("#commit-chart");

        // draws the commit chart
        commitChart.weekchart({
            value: elementContents
        });
    });

    // starts the panel rotation for the body
    _body.panelrotation();
});

var messageProcessor = function(data) {
    // parses the data retrieving the json
    var jsonData = jQuery.parseJSON(data);

    // retrieves the message id and contents
    var messageId = jsonData["id"];
    var messageContents = jsonData["contents"];

    // switches over the message id
    switch (messageId) {
        case "medium/field/set":
            // parses the data (json) retrieving the status
            var status = jQuery.parseJSON(messageContents);

            // retrieves the key
            var key = status["key"];

            // retrieves the value
            var value = status["value"];

            // sets the field
            setField(key, value);

            // breaks the switch
            break;

        case "medium/message/new":
            // parses the data (json) retrieving the status
            var status = jQuery.parseJSON(messageContents);

            // retrieves the value
            var value = status["value"];

            // retrieves the type
            var type = status["type"];

            // retrieves the hide
            var hide = status["hide"];

            // shows the given message
            showMessage(value, type, hide);

            // breaks the switch
            break;

        case "medium/video/new":
            // parses the data (json) retrieving the status
            var status = jQuery.parseJSON(messageContents);

            // retrieves the video id
            var videoId = status["video_id"];

            // shows the given video id
            showVideo(videoId);

            // breaks the switch
            break;

        case "medium/ticker_message/new":
            // parses the data (json) retrieving the status
            var status = jQuery.parseJSON(messageContents);

            // retrieves the value
            var value = status["value"];

            // retrieves the type
            var type = status["type"];

            // retrieves the sub value
            var subValue = status["sub_value"];

            // shows the given ticker message
            addTickerMessage(value, type, subValue);

            // breaks the switch
            break;

        case "medium/ticker_message/clear":
            // parses the data (json) retrieving the status
            var status = jQuery.parseJSON(messageContents);

            // shows the given ticker message
            clearTicker();

            // breaks the switch
            break;
    }
}

var setField = function(key, value) {
    // retrieves the body element
    var _body = jQuery("body");

    // retrieves the key value element
    var keyValueElement = jQuery("#" + key + "-value");

    // updates the key value element value
    keyValueElement.html(value);

    // triggers the set field event
    _body.trigger("set_field", [key, value]);

    // triggers the set field (composite) event
    _body.trigger("set_field_" + key, [key, value]);
}

var showMessage = function(value, type, hide) {
    // retrieves the content wrapper element
    var contentWrapper = jQuery("#content-wrapper");

    // removes the current window (if any)
    contentWrapper.window("remove");

    // shows the message window
    contentWrapper.window();

    // retrieves the created content wrapper window element
    var contentWrapperWindow = jQuery("#content-wrapper .window");

    // converts the window to message window
    contentWrapperWindow.messagewindow("default", {
        value: value,
        type: type,
        hide: hide
    });

    // centers the video window
    contentWrapper.window("center");
}

var showVideo = function(videoId) {
    // retrieves the content wrapper element
    var contentWrapper = jQuery("#content-wrapper");

    // removes the current window (if any)
    contentWrapper.window("remove");

    // shows the video window
    contentWrapper.window();

    // retrieves the created content wrapper window element
    var contentWrapperWindow = jQuery("#content-wrapper .window");

    // converts the window to video window
    contentWrapperWindow.videowindow();
    contentWrapperWindow.videowindow("setVideo", {
        videoId: videoId
    });

    // centers the video window
    contentWrapper.window("center");
}

var addTickerMessage = function(value, type, subValue) {
    // retrieves the ticker element
    var ticker = jQuery("#ticker");

    // retrieves the main panel
    var mainPanel = jQuery("#main-panel");

    // determines if the main panel is visible
    var mainPanelVisible = mainPanel.is(":visible");

    // in case the main panel is not visible shows it
    !mainPanelVisible && mainPanel.show();

    // adds the message to the ticker
    ticker.ticker("add", {
        value: value,
        type: type,
        subValue: subValue
    });

    // in case the main panel was not visible hides it
    !mainPanelVisible && mainPanel.hide();
}

var clearTicker = function() {
    // retrieves the ticker element
    var ticker = jQuery("#ticker")

    // clears the ticker
    ticker.ticker("clear");
}

var onYouTubePlayerReady = function(playerId) {
    // retrieves the video contents element
    var videoContentsElement = jQuery("#video-contents")

    // retrieves the video contents reference
    var videoContentsReference = videoContentsElement.get(0);

    // adds the on state change event listener
    videoContentsReference.addEventListener("onStateChange",
        "onYouTubeStateChange");
}

var onYouTubeStateChange = function(newState) {
    // retrieves the content wrapper element
    var contentWrapper = jQuery("#content-wrapper");

    // in case the video has ended
    if (newState === 0) {
        // removes the current video window
        contentWrapper.window("remove");
    }
}
