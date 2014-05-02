$(function() {
  var Task = Backbone.Model.extend({
    defaults: {text: '', completed: false},
    urlRoot: '/tasks',

    toggle: function() {
      this.save({completed: this.attributes.completed ? 0 : 1});
    }
  });

  var TaskList = Backbone.Collection.extend({
    model: Task,
    url: '/tasks'
  });

  var TaskView = Backbone.View.extend({
    tagName: "li",

    events: {
      "click .toggle" : "toggleComplete"
    },

    template: _.template($('#task-template').html()),

    toggleComplete: function() {
      this.model.toggle();
      this.render();
    },

    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
     }
   });

  var AppView = Backbone.View.extend({
    el: $("#tasks-app"),

    events: {
      "click #create-task": "createTask",
      "keypress #create-task-text":  "createTaskOnEnter",
    },

    initialize: function() {
      this.listenTo(Tasks, 'add',   this.addTask);
      this.listenTo(Tasks, 'reset', this.addTasks);
      this.listenTo(Tasks, 'all',   this.render);

      Tasks.fetch();
    },

    createTaskOnEnter: function(e) {
      if (e.keyCode === 13) { this.createTask(); }
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

    addTasks: function() { Tasks.each(this.addTask, this); }
  });

  var Tasks = new TaskList;
  var App   = new AppView;
});
