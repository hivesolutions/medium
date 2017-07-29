// Hive Solutions Development
// Copyright (c) 2008-2017 Hive Solutions Lda.
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
// __copyright__ = Copyright (c) 2008-2017 Hive Solutions Lda.
// __license__   = Hive Solutions Confidential Usage License (HSCUL)

(function(jQuery) {
    jQuery.fn.panelrotation = function(method, options) {
        // the default timeout for rotation
        var DEFAULT_TIMEOUT = 30000;

        // the default values for the panel rotation
        var defaults = {
            timeout: DEFAULT_TIMEOUT
        };

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            // retrieves the panels
            var panels = jQuery(".panel", matchedObject);

            // initializes the element ids list
            var elementIds = [];

            // iterates over all the panels to create
            // the initial element ids (list)
            panels.each(function(index, element) {
                // retrieves the element
                var element = jQuery(this);

                // retrieves the element id
                var elementId = element.attr("id");

                // in case the current element
                // is the main panel
                if (elementId === "main-panel") {
                    // continues the loop
                    return;
                }

                // adds the element id to the list
                // of element ids
                elementIds.push(elementId);
            });

            // sets the initial show main value
            matchedObject.data("showMain", true);

            // sets the initial current index value
            matchedObject.data("currentIndex", 0);

            // sets the element ids (list) value
            matchedObject.data("elementIds", elementIds);
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // runs the initial update for the matched object
            _update(matchedObject, options);
        };

        var _update = function(matchedObject, options) {
            // retrieves the timeout value
            var timeout = options["timeout"];

            // retrieves the show main value
            var showMain = matchedObject.data("showMain");

            // retrieves the current index value
            var currentIndex = matchedObject.data("currentIndex");

            // retrieves the element ids list
            var elementIds = matchedObject.data("elementIds");

            // in case the show main is set
            if (showMain === true) {
                // retrieves the current element as the main panel
                var currentElement = jQuery("#main-panel", matchedObject);

                // unsets the show main value
                matchedObject.data("showMain", false);
            } else {
                // in case the current index "overflows"
                if (currentIndex === elementIds.length) {
                    // resets the current index
                    currentIndex = 0;
                }

                // retrieves the current element id
                var currentElementId = elementIds[currentIndex];

                // retrieves the current element
                var currentElement = jQuery("#" + currentElementId,
                    matchedObject);

                // increments the current index
                currentIndex++;

                // sets the show main value
                matchedObject.data("showMain", true);

                // updates the current index value
                matchedObject.data("currentIndex", currentIndex);
            }

            // retrieves the panel elements
            var panelElements = jQuery(".panel", matchedObject);

            // fades out the panels and fades in the current
            // element
            panelElements.fadeOut(300);
            currentElement.fadeIn(300);

            // sets the timeout for the update
            setTimeout(function() {
                _update(matchedObject, options)
            }, timeout);
        };

        // switches over the method
        switch (method) {
            case "default":
                // initializes the plugin
                initialize();

                // breaks the switch
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.scheduler = function(method, options) {
        // the scheduler rate (number ticks per second)
        var SCHEDULER_RATE = 300;

        // the scheduler rate timeout, calculated from the
        // scheduler rate
        var SCHEDULER_RATE_TIMEOUT = 1000 / SCHEDULER_RATE;

        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            // creates the queue list
            matchedObject.data("queueList", []);
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // starts the update cycle
            _update(matchedObject, options);
        };

        var _update = function(matchedObject, options) {
            // updates the values (inner method)
            __update(matchedObject, options);

            // sets the timeout for the next update
            setTimeout(function() {
                _update(matchedObject, options);
            }, SCHEDULER_RATE_TIMEOUT);
        };

        var _add = function(matchedObject, options) {
            // retrieves the queue list
            var queueList = matchedObject.data("queueList");

            // retrieves the item
            var item = options["item"];

            // inserts the item into the queue list
            queueList.splice(0, 0, item);
        };

        var __update = function(matchedObject, options) {
            // retrieves the queue list
            var queueList = matchedObject.data("queueList");

            // retrieves the current date
            var currentDate = new Date();

            // retrieves the current timestamp
            var currentTimestamp = currentDate.getTime();

            // retrieves the current top element
            var currentElement = queueList[0];

            // in case the current element target timestamp
            // is valid (is time to execute it)
            if (currentElement && currentElement.targetTimestamp <= currentTimestamp) {
                // calls the method associated with
                // the current element
                currentElement.method(currentElement);

                // pops the queue list
                queueList.pop();
            }
        };

        // switches over the method
        switch (method) {
            case "add":
                _add(matchedObject, options);
                break;

            case "default":
                // initializes the plugin
                initialize();
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.time = function(method, options) {
        // the update timeout
        var UPDATE_TIMEOUT = 100;

        // the list of abreviated names for the months
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec"
        ];

        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {};

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // starts the update time cycle
            _updateTime(matchedObject, options);
        };

        var _updateTime = function(matchedObject, options) {
            // updates the time (inner method)
            __updateTime(matchedObject, options);

            // sets the timeout for the next time update
            setTimeout(function() {
                _updateTime(matchedObject, options);
            }, UPDATE_TIMEOUT);
        };

        var __updateTime = function(matchedObject, options) {
            // retrieves the date time element
            var dateTimeElement = jQuery("#date-time", matchedObject);

            // retrieves the time element
            var timeElement = jQuery(".time", matchedObject);

            // retrieves the current date
            var currentDate = new Date();

            // retrieves the date information
            var year = currentDate.getYear();
            var month = currentDate.getMonth();
            var day = currentDate.getDate();

            // retrieves the time information
            var hours = currentDate.getHours();
            var minutes = currentDate.getMinutes();
            var seconds = currentDate.getSeconds();

            // normalizes the date information
            var normalizedYear = 1900 + year;
            var monthName = MONTHS[month];

            // converts the values to string
            // with rounded value
            day = __numberToString(day, 2)
            hours = __numberToString(hours, 2)
            minutes = __numberToString(minutes, 2)
            seconds = __numberToString(seconds, 2)

            // retrieves the date element
            var dateElement = jQuery(".date", dateTimeElement);

            // retrieves the hour element
            var hourElement = jQuery("#hour", timeElement);

            // retrieves the minute element
            var minuteElement = jQuery("#minute", timeElement);

            // retrieves the second element
            var secondElement = jQuery("#second", timeElement);

            // updates the date element
            dateElement.html(day + " " + monthName + " " + normalizedYear);

            // updates the time elements
            hourElement.html(String(hours));
            minuteElement.html(String(minutes));
            secondElement.html(String(seconds));
        };

        var __numberToString = function(number, minimumCharacters) {
            // converts the number into a string
            var numberString = String(number);

            // iterates while there are characters
            // in the number string
            while (numberString.length < minimumCharacters) {
                // prepends a zero to the number string
                numberString = "0" + numberString;
            }

            // returns the number in string format
            return numberString;
        };

        // switches over the method
        switch (method) {
            case "default":
                // initializes the plugin
                initialize();
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.window = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            matchedObject.append("<div class=\"window\"></div>");

            // centers the window
            _centerWindow(matchedObject, options);
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            jQuery(window).resize(function(event) {
                // centers the window
                _centerWindow(matchedObject, options);
            });
        };

        var _centerWindow = function(matchedObject, options) {
            // retrieves the window element
            var windowElement = jQuery(".window", matchedObject);

            // retrieves the window
            var _windowElement = jQuery(window);

            // retrieves the window dimensions
            var _windowWidth = _windowElement.width();
            var _windowHeight = _windowElement.height();

            // retrieves the window width and height
            var windowWidth = windowElement.width();
            var windowHeight = windowElement.height();

            // retrieves the window offset
            var windowOffset = windowElement.offset();

            // calculates the window top (y) and left (x) position
            var windowY = (_windowHeight / 2) - (windowHeight / 2);
            var windowX = (_windowWidth / 2) - (windowWidth / 2);

            // sets the window top and left position
            windowElement.css("top", windowY + "px");
            windowElement.css("left", windowX + "px");
        };

        var _removeWindow = function(matchedObject, options) {
            // retrieves the window element
            var windowElement = jQuery(".window", matchedObject);

            // removes the window element
            windowElement.remove();
        };

        // switches over the method
        switch (method) {
            case "center":
                _centerWindow(matchedObject, options);
                break;

            case "remove":
                _removeWindow(matchedObject, options);
                break;

            case "default":
                // initializes the plugin
                initialize();
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.messagewindow = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            // retrieves the value
            var value = options["value"] ? options["value"] : "invalid";

            // retrieves the type
            var type = options["type"] ? options["type"] : "information";

            // retrieves the secure
            var secure = options["secure"] ? options["secure"] : true;

            // creates the validation regex
            var validationRegex = new RegExp("[^<>]+");

            // tries to match the value against the
            // validation regex
            var valueMatch = value.match(validationRegex);

            // in case the match is not valid and the secure
            // flag is enabled
            if (secure && (valueMatch === null || valueMatch === undefined || valueMatch[0] !== value)) {
                // sets the value to invalid message
                value = "invalid message sent";
            }

            // switches over the type
            switch (type) {
                case "error":
                    var audioSource = "resources/audio/error.ogg";
                    var iconClass = "icon-error";
                    var extraClass = "orange-background";
                    break;

                case "warning":
                    var audioSource = "resources/audio/warning.ogg";
                    var iconClass = "icon-warning";
                    var extraClass = "yellow-background";
                    break;

                case "information":
                    var audioSource = "resources/audio/information.ogg";
                    var iconClass = "icon-information";
                    var extraClass = "blue-background";
                    break;
            }

            matchedObject.append("<div class=\"message-box-contents\">" + "<div class=\"icon text-header " +
                iconClass + "\">" + type + "</div>" + "<p class=\"text text-message\">" + value +
                "</p>" + "<audio src=\"" + audioSource + "\" autoplay=\"autoplay\">" + "</div>");

            matchedObject.addClass("message-box");
            matchedObject.addClass(extraClass);
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // retrieves the hide
            var hide = options["hide"] ? options["hide"] : 10000;

            // in case the hide variable is set
            // sets the timeout for the hide and remove
            // of the window
            hide && setTimeout(function() {
                // hides and removes the window
                __hideRemoveWindow(matchedObject, options);
            }, hide);
        };

        var __hideRemoveWindow = function(matchedObject, options) {
            // hides the current window
            matchedObject.fadeOut(500, function() {
                // removes the window
                matchedObject.remove();
            });
        };

        // switches over the method
        switch (method) {
            case "default":
                // initializes the plugin
                initialize();
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.videowindow = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            matchedObject.append("<div id=\"video-box-contents\"></div>");
            matchedObject.addClass("video-box");
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {};

        var _setVideo = function(matchedObject, options) {
            // retrieves the video id
            var videoId = options["videoId"];

            // creates the parameters map
            var parameters = {
                allowScriptAccess: "always",
                allowfullscreen: "true",
                width: "100%",
                height: "100%"
            };

            // creates the attributes map
            var attributes = {
                id: "video-contents"
            };

            // creates the complete video url
            var url = "http://www.youtube.com/v/" + videoId +
                "?fs=1&rel=0&enablejsapi=1&version=3&amp;hl=en_US&amp;hd=1;autoplay=1";

            // embeddeds the swf for the video
            swfobject.embedSWF(url, "video-box-contents", "100%", "100%", "8",
                null, null, parameters, attributes);
        };

        // switches over the method
        switch (method) {
            case "setVideo":
                _setVideo(matchedObject, options);
                break;

            case "default":
                // initializes the plugin
                initialize();
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.ticker = function(method, options) {
        // the frame rate (number frames per second)
        var FRAME_RATE = 120;

        // the frame rate timeout, calculated from the
        // scheduler rate
        var FRAME_RATE_TIMEOUT = 1000 / FRAME_RATE;

        // the speed of the ticker
        var SPEED = 150;

        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            // resizes the ticker
            _resize(matchedObject, options);

            // schedules the first iteration the ticker
            __scheduleIteration(matchedObject, options, 0);
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {};

        var _resize = function(matchedObject, options) {
            // retrieves the ticker wrapper element
            var tickerWrapperElement = jQuery("#ticker-wrapper", matchedObject);

            // retrieves the ticker reference
            var tickerReference = matchedObject.get(0);

            // retrieves the ticker width
            var tickerWidth = tickerReference.offsetWidth;

            // calculates the toal width
            var totalWidth = __calculateTotalWidth(matchedObject, options);

            // sets the width and padding left of the ticker wrapper
            // element
            tickerWrapperElement.css("width", totalWidth + tickerWidth + "px");
            tickerWrapperElement.css("padding-left", tickerWidth + "px");

            // sets the total width in the matched object
            matchedObject.data("totalWidth", totalWidth);

            // retrieves the reset position value
            var resetPosition = options["resetPosition"];

            // resets the scroll left
            tickerReference.scrollLeft = 0;
        };

        var _updatePosition = function(item) {
            // retrieves the item arguments
            var arguments = item.arguments;

            // retrieves the matched object
            var matchedObject = arguments["matchedObject"];

            // retrieves the options
            var options = arguments["options"];

            // retrieves the target scroll
            var targetScroll = arguments["targetScroll"];

            // retrieves the total width from the matched object
            var totalWidth = matchedObject.data("totalWidth");

            // retrieves the reset position flag from the matched object
            var resetPosition = matchedObject.data("resetPosition");

            // retrieves the current date
            var currentDate = new Date();

            // retrieves the current timestamp
            var currentTimestamp = currentDate.getTime();

            // calculates the increment to be used
            var increment = SPEED / FRAME_RATE;

            // retrieves the ticker element
            var tickerElement = jQuery("#ticker");

            // retrieves the ticker reference
            var tickerReference = tickerElement.get(0)

            // in case the "frame" is not to be skipped
            if (currentTimestamp < item.targetTimestamp + FRAME_RATE_TIMEOUT) {
                //sets the new scroll left
                tickerReference.scrollLeft = targetScroll
            }

            // sets the current scroll
            var currentScroll = targetScroll;

            // retrieves the current width
            var currentWidth = tickerReference.offsetWidth

            // calculates the view width from the current
            // width and the total width
            var viewWidth = currentWidth + totalWidth;

            // in case the current scroll is greater
            // than the view width (collision test) or the reset
            // position flag is set
            if (currentScroll >= viewWidth || resetPosition) {
                // resets the scroll left
                tickerReference.scrollLeft = 0;

                // sets (updates) the current scroll
                currentScroll = 0;

                // unsets the reset position flag
                resetPosition = false;
            }

            // calculates the target scroll
            var targetScroll = currentScroll + increment;

            // schedules the iteration
            __scheduleIteration(matchedObject, options, targetScroll);

            // sets the reset position value
            matchedObject.data("resetPosition", resetPosition);
        };

        var _add = function(matchedObject, options) {
            // retrieves the value
            var value = options["value"];

            // retrieves the type
            var type = options["type"];

            // retrieves the sub value
            var subValue = options["subValue"];

            // retrieves the ticker wrapper element
            var tickerWrapperElement = jQuery("#ticker-wrapper", matchedObject);

            // retrieves the ticker reference
            var tickerReference = matchedObject.get(0);

            // switches over the type
            switch (type) {
                case "error":
                    var iconClass = "icon-ticker-error";
                    var subValueClass = "orange";
                    break;

                case "warning":
                    var iconClass = "icon-ticker-warning";
                    var subValueClass = "yellow";
                    break;

                case "information":
                    var iconClass = "icon-ticker-information";
                    var subValueClass = "blue";
                    break;
            }

            // retrieves the ticker wrapper icon tickers
            var tickerWrapperIconTickers = tickerWrapperElement.children(".icon-ticker");

            // retrieves if the ticker wrapper is empty
            var tickerWrapperElementEmpty = tickerWrapperIconTickers.length === 0;

            // retrieves the ticker wrapper clear element
            var tickerWrapperClearElement = jQuery(".clear",
                tickerWrapperElement);

            // adds the ticker before the clear element
            tickerWrapperClearElement.before("<div class=\"icon-ticker " + iconClass + "\">" +
                "<span class=\"text\">" + value + "</span> " + "<span class=\"sub-header-ticker " +
                subValueClass + "\">" + subValue + "</span>" + "</div>");

            // retrieves the icon ticker element
            var iconTicketElement = jQuery(
                "#ticker-wrapper > .icon-ticker:last", matchedObject);

            // retrieves the ticker width
            var tickerWidth = tickerReference.offsetWidth;

            // calculates the total width
            var totalWidth = __calculateTotalWidth(matchedObject, options);

            // sets the width of the ticker wrapper element
            tickerWrapperElement.css("width", totalWidth + tickerWidth + "px");

            // sets the reset position flag, in case the
            // ticker wrapper element was empty (before)
            tickerWrapperElementEmpty
                && matchedObject.data("resetPosition", true);

            // sets the total width in the matched object
            matchedObject.data("totalWidth", totalWidth);
        };

        var _clear = function(matchedObject, options) {
            // retrieves the ticker wrapper icon tickers
            var tickerWrapperIconTickers = jQuery(
                "#ticker-wrapper > .icon-ticker", matchedObject);

            // removes the icon tickers
            tickerWrapperIconTickers.remove();
        };

        var __scheduleIteration = function(matchedObject, options, targetScroll) {
            // retrieves the current date
            var currentDate = new Date();

            // retrieves the current tiestamp
            var currentTimestamp = currentDate.getTime();

            // creates the item (map)
            var item = {}

            // sets the item properties
            item.targetTimestamp = currentTimestamp + FRAME_RATE_TIMEOUT
            item.method = _updatePosition;
            item.arguments = {
                matchedObject: matchedObject,
                options: options,
                targetScroll: targetScroll
            };

            // adds the item to the scheduler
            jQuery("body").scheduler("add", {
                item: item
            });
        };

        var __calculateTotalWidth = function(matchedObject, options) {
            // retrieves the icon ticker element
            var iconTickerElement = jQuery(".icon-ticker", matchedObject);

            // starts the total width value
            var totalWidth = 0;

            // iterates over all the icon ticker elements
            iconTickerElement.each(function(index, element) {
                // retrieves the current element
                var currentElement = jQuery(element);

                // retrieves the element offsert width
                var elementOffsetWidth = element.offsetWidth;

                // calculates the element margin
                var currentElementMarginLeft = parseInt(currentElement.css("margin-left"))
                var currentElementMarginRight = parseInt(currentElement.css("margin-right"))

                // increments the total width with the element offset width
                // and the current element margins
                totalWidth += elementOffsetWidth + currentElementMarginLeft +
                    currentElementMarginRight;
            });

            // returns the total width
            return totalWidth;
        };

        // switches over the method
        switch (method) {
            case "add":
                _add(matchedObject, options);
                break;

            case "clear":
                _clear(matchedObject, options);
                break;

            case "default":
                // initializes the plugin
                initialize();
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.error = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {};

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {

        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {};

        var _show = function(matchedObject, options) {
            // retrieves the message
            var message = options["message"];

            // retrieves the overlay
            var overlay = jQuery(".overlay", matchedObject);

            // retrieves the error message
            var errorMessage = jQuery(".error .message", matchedObject);

            // sets the error message
            errorMessage.html(message);

            // shows the overlay
            overlay.fadeIn(1000);
        };

        var _hide = function(matchedObject, options) {
            // retrieves the overlay
            var overlay = jQuery(".overlay", matchedObject);

            // hides the overlay
            overlay.fadeOut(500);
        };

        // switches over the method
        switch (method) {
            case "show":
                // shows the error
                _show(matchedObject, options);

                // breaks the switch
                break;

            case "hide":
                // hides the error
                _hide(matchedObject, options);

                // breaks the switch
                break;

            case "default":
                // initializes the plugin
                initialize();

                // breaks the switch
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.weekchart = function(options) {
        // the list of abreviated names for the months
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec"
        ];

        // the default value to be used
        var DEFAULT_VALUE = {};

        // the default timeout to be used for drawing the commit
        // chart (avoids problems while loading remote fonts)
        var DEFAULT_TIMEOUT = 1000;

        // the default values for the menu
        var defaults = {
            value: DEFAULT_VALUE,
            timeout: DEFAULT_TIMEOUT
        };

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            // retrieves the value
            var value = options["value"];

            // retrieves the timeout
            var timeout = options["timeout"];

            // parses the value retrieving the values
            var values = jQuery.parseJSON(value);

            // creates the options map
            var _options = {};

            // creates the data map
            var data = {};

            // starts the list of labels
            labels = [];

            // iterates over all the keys in the values
            // to sets the labels
            for (var key in values) {
                // adds teh key to the list of labels
                labels.push(key);
            }

            // starts the list of horizontal labels
            horizontalLabels = [""];

            // retrieves the "initial" date
            var initiaDate = new Date();

            // retrieves the current timestamp
            var initialTimestamp = initiaDate.getTime();

            // iterates over the seven days to follow
            for (var index = 6; index >= 0; index--) {
                // retrieves the current timestamp (from the initial
                // timestamp)
                var currentTimestamp = initialTimestamp - (index * 86400000);

                // creates a "new" date and sets the
                // current (iteration) timestamp
                var newDate = new Date();
                newDate.setTime(currentTimestamp);

                // retrieves the month day and index from
                // the new date
                var monthDay = newDate.getUTCDate();
                var monthIndex = newDate.getUTCMonth();

                // retrieves the month name from using the month index
                var monthName = MONTHS[monthIndex];

                // converts the month day to string
                var monthDayString = String(monthDay);

                // creates the month label by appending the month
                // day to the month name
                var monthLabel = monthDayString + monthName;

                // adds the month label to the list of horizontal labels
                horizontalLabels.push(monthLabel);
            }

            // sets the values in the data
            data["values"] = values;

            // sets the labels in the data
            data["labels"] = labels;

            // sets the horizontal labels in the data
            data["horizontalLabels"] = horizontalLabels;

            // sets the data in the chart map
            _options["data"] = data;

            // sets the timeout to draw the chart
            // avoids problems while loading remote fonts
            setTimeout(function() {
                // draws the chart
                matchedObject.chart("draw", _options);
            }, timeout);
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {};

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);
