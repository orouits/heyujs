'use strict';

// Application
var app = angular.module('heyujs', [
    'ngRoute',
    'ngResource',
    'ngMaterial'
]);

// Router
app.config(function($routeProvider) {
    $routeProvider
    .when("/home", {
        templateUrl: 'web/js/homeView.html',
        controller: 'homeCtrl',
        name:"Home",
        icon:"home"
    })
    .when("/units", {
        templateUrl: 'web/js/unitsView.html',
        controller: 'unitsCtrl',
        name:"Units",
        icon:"view_modules"
    })
    .when("/aliases", {
        templateUrl: 'web/js/aliasesView.html',
        controller: 'aliasesCtrl',
        name:"Aliases",
        icon:"cast_connected"
    })
    .when("/schedules", {
        templateUrl: 'web/js/schedulesView.html',
        controller: 'schedulesCtrl',
        name:"Schedules",
        icon:"schedule"
    })
    .when("/settings", {
        templateUrl: 'web/js/settingsView.html',
        controller: 'settingsCtrl',
        name:"Settings",
        icon:"settings"
    })
    .when("/commands", {
        templateUrl: 'web/js/commandsView.html',
        controller: 'commandsCtrl',
        name:"Commands",
        icon:"build"
    })
    .otherwise({
        redirectTo: '/home'
    })
    ;
});
