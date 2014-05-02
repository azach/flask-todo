$(function() {
  var Task = Backbone.Model.extend({
    defaults: {text: '', completed: false},
    urlRoot: '/tasks',

    toggle: function() {
      this.save({completed: !this.attributes.completed});
    }
  });

  var TaskList = Backbone.Collection.extend({
    model: Task,
    url: '/tasks',
    remaining: function() {
      return this.where({completed: false});
    }
  });

  var TaskView = Backbone.View.extend({
    tagName: "li",

    events: {
      "click .toggle" : "toggleComplete"
    },

    template: _.template($('#task-template').html()),

    toggleComplete: function() { this.model.toggle(); },

    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
    },

    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
     }
   });

  var AppView = Backbone.View.extend({
    el: $("#tasks-app"),

    footerTemplate: _.template($('#footer-template').html()),

    events: {
      "click #mark-all-complete": "toggleAllComplete",
      "click #create-task": "createTask",
      "keypress #create-task-text":  "createTaskOnEnter",
    },

    initialize: function() {
      this.listenTo(Tasks, 'add',   this.addTask);
      this.listenTo(Tasks, 'reset', this.addTasks);
      this.listenTo(Tasks, 'all',   this.render);

      this.footer = this.$('#tasks-footer');

      Tasks.fetch();
    },

    render: function() {
      this.footer.html(this.footerTemplate({remaining: Tasks.remaining().length}));
    },

    createTaskOnEnter: function(e) {
      if (e.keyCode === 13) {
        e.preventDefault();
        this.createTask();
      }
    },

    createTask: function() {
      $input = this.$el.find('#create-task-text');
      if (!$input.val()) { return; }
      Tasks.create({text: $input.val()});
      $input.val('');
    },

    addTask: function(task) {
      var view = new TaskView({model: task});
      this.$("#task-list").append(view.render().el);
    },

    addTasks: function() { Tasks.each(this.addTask, this); },

    toggleAllComplete: function (e) {
      e.preventDefault();
      _.each(Tasks.remaining(), function(task) { task.toggle(); });
    }
  });

  var Tasks = new TaskList;
  var App   = new AppView;
});
