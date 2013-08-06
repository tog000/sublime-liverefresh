module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      liverefresh:{
        files: {
          'js/liverefresh.min.js': ['js/liverefresh.js'],
        },
      },
    },
    watch: {
      scripts: {
        files: ['js/*.js'],
        tasks: ['jshint','uglify'],
        options: {
          spawn: false,
        },
      },
    },
    jshint: {
      files: ['js/*.js'],
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-jshint');

  // Default task(s).
  grunt.registerTask('default', ['uglify']);

};