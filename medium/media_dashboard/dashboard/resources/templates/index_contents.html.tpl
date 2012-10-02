<div class="overlay">
    <div class="error">
        <img src="${out_none value=base_path /}resources/images/broken-transmission.png" />
        <p class="title">Something went terribly wrong</p>
        <p class="message">${out_none value=exception_message xml_escape=True /}</p>
    </div>
</div>
<div class="fields">
    ${foreach item=field_value key=field_key from=fields_map}
        <div id="field-${out_none value=field_key xml_escape=True /}">${out_none value=field_value xml_escape=True /}</div>
    ${/foreach}
</div>
<div id="commit-chart-panel" class="panel">
    <div class="title-container" class="chart-container">
        <p class="header yellow">commits progress/<span class="sub-header">/7 days</span></p>
    </div>
    <div id="commit-chart-container" class="chart-container">
        <canvas id="commit-chart" class="chart" width="1680" height="900"></canvas>
    </div>
</div>
<div id="bargania-chart-panel" class="panel">
    <div class="title-container" class="chart-container">
        <p class="header yellow">bargania progress/<span class="sub-header">/7 days</span></p>
    </div>
    <div id="bargania-chart-container" class="chart-container">
        <canvas id="bargania-chart" class="chart" width="1680" height="900"></canvas>
    </div>
</div>
<div id="main-panel" class="panel">
    <div id="main-wrapper">
        <div id="left">
            <div id="logo"></div>
            <div id="date-time">
                <p class="date"></p>
                <span class="time">
                    <span id="hour"></span>:<span id="minute"></span>:<span id="second"></span>
                </span>
            </div>
        </div>
        <div id="right">
            <div id="commits">
                <p class="header yellow">commits <span class="sub-header">/24h</span></p>
                <span id="commits-value" class="stat">${out_none value=fields_map.commits xml_escape=True /}</span>
            </div>
            <div id="bugs">
                <p class="header purple">bugs <span class="sub-header">/24h</span></p>
                <span id="bugs-value" class="stat">${out_none value=fields_map.bugs xml_escape=True /}</span>
            </div>
            <div id="elcommitator" class="clear">
                <p class="header"><span class="header blue">commiter of the day</span></p>
                <span id="commiter-value" class="text-header">${out_none value=fields_map.commiter xml_escape=True /}</span><span class="sub-header-commit">/<span id="commiter_count-value">${out_none value=fields_map.commiter_count xml_escape=True /}</span> commits</span>
            </div>
        </div>
    </div>
    <div class="clear"></div>
    <div id="ticker">
        <div id="ticker-wrapper">
            ${foreach item=ticker_message from=ticker_messages}
                ${if item=ticker_message.type value="error" operator="eq"}
                    <div class="icon-ticker icon-ticker-error">
                        <span class="text">${out_none value=ticker_message.value xml_escape=True /}</span>
                        <span class="sub-header-ticker orange">${out_none value=ticker_message.sub_value xml_escape=True /}</span>
                    </div>
                ${elif item=ticker_message.type value="warning" operator="eq" /}
                    <div class="icon-ticker icon-ticker-warning">
                        <span class="text">${out_none value=ticker_message.value xml_escape=True /}</span>
                        <span class="sub-header-ticker yellow">${out_none value=ticker_message.sub_value xml_escape=True /}</span>
                    </div>
                ${elif item=ticker_message.type value="information" operator="eq" /}
                    <div class="icon-ticker icon-ticker-information">
                        <span class="text">${out_none value=ticker_message.value xml_escape=True /}</span>
                        <span class="sub-header-ticker blue">${out_none value=ticker_message.sub_value xml_escape=True /}</span>
                    </div>
                ${/if}
            ${/foreach}
            <div class="clear"></div>
        </div>
    </div>
</div>
