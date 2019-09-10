app.factory('unitService', ['$resource', function($resource){
    return $resource('api/units/:id',{id:'@id'},
        { 
            config: {method: 'PATCH'}
        }
    ); 
}]);

app.factory('settingService', ['$resource', function($resource){
    return $resource('api/settings/:id',{id:'@id'});
}]);

app.factory('aliasService', ['$resource', function($resource){
    return $resource('api/aliases/:id',{id: "@id"});
}]);

app.factory('scheduleService', ['$resource',function($resource){
    return $resource('api/schedules/:id',{id:'@id'});
}]);

app.factory('macroService', ['$resource',function($resource){
    return $resource('api/macros/:id',{id:'@id'});
}]);

app.factory('commandService', ['$resource', function($resource){
    var commandService = $resource('api/commands/',
        null, 
        { 
            query: {method: 'GET', isArray:false}
        }
    );
    return commandService;
}]);

app.factory('statusService', ['$resource', function($resource){
    var statusService = $resource('api/status/',
        null, 
        { 
            query: {method: 'GET', isArray:false}
        }
    );
    return statusService;
}]);
