search_wiki_payload = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*`/searchwiki <Search Term>`*\nReturns the summary of the Wikipedia article matching the *<Search Term>*\nEg., /searchwiki Slack"
			}
		}
	]
}


random_wiki_payload = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*`/randomwiki`*\nReturns the summary of a random Wikipedia article"
			}
        }
	]
}


today_wiki_payload = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*`/todaywiki`*\nReturns the events for the current day"
			}
		}
	]
}


geosearch_wiki_payload = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*`/geosearchwiki /geosearchwiki --lat=<latitude> --lon=-<longitude> --lat=37.75 --lon=-122.2833`*\nReturns the Wikipedia article matching the Geographic coordinate. If *--lat* or *--lon* is skipped, *_0.0_* is taken as the default value\nEg., /geosearchwiki --lat=37.75 --lon=-122.2833"
			}
		}
	]
}


help_wiki_payload = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Ahoy! Welcome to *WikiBot*\nWikiBot helps you to get information from Wikipedia directly from Slack\n\n_*These are the following commands supported in WikiBot*_"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*`/searchwiki <Search Term>`*\nReturns the summary of the Wikipedia article matching the *<Search Term>*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*`/randomwiki`*\nReturns the summary of a random Wikipedia article"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*`/todaywiki`*\nReturns the events for the current day"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*`/geosearchwiki --lat=<latitude> --lon=-<longitude>`*\nReturns the Wikipedia article matching the Geographic coordinate. If *--lat* or *--lon* is skipped, *_0.0_* is taken as the default value"
			}
		}
	]
}


invalid_command_payload = {
    "blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Oops! Looks like you entered a command which is not supported by *WikiBot*\n\nUse `/helpwiki` to get the list of supported commands"
			}
		}
    ]
}