App = Ember.Application.create();
App.deferReadiness();
App.feeds = [];
$.getJSON("/feeds.json", function( data ) {
	App.feeds = data;
	App.advanceReadiness();
});
App.Router.map(function() {
  this.resource("about");
  this.resource("feeds", function() {
    this.resource("feed", {path: ":feed_title"});
  });
});

App.IndexRoute = Ember.Route.extend({
    redirect: function() {
      this.transitionTo("feed");
    }
});

App.FeedsRoute = Ember.Route.extend({
  model: function() {
    return App.feeds;
  }
});

App.FeedRoute = Ember.Route.extend({
	model: function(params) {
		var items = getFeedByTitle(params.feed_title);
	      return items;
}
});

App.AboutRoute = Ember.Route.extend({
    model: function() {
      return ["Black", "Red", "Blue"];
    }
});

function getFeedByTitle(title) {
	for (var i = 0; i<App.feeds.length; i++) {
		if (App.feeds[i].title == title) {
			return App.feeds[i];
		}
	}
}

