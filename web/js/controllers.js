app.controller('appCtrl', ['$scope', '$route', '$mdSidenav', 'statusService', 'commandService',function($scope, $route, $mdSidenav, statusService, commandService) {
    $scope.$route=$route;
    
    statusService.query({}, function(result) {
        $scope.status = result.status;
    });
    
    // compute the valid configured route array from $route to generate the sidenav menu
    $scope.validRoutes = [];
    Object.keys($route.routes).forEach(function(key) {
        var val = $route.routes[key];
        if (val.hasOwnProperty('name'))
            $scope.validRoutes.push(val);
    });
 
    $scope.openSide = function() {
        $mdSidenav('left').open();
    };
    $scope.closeSide = function() {
        $mdSidenav('left').close();
    };
    $scope.start = function() {
        $scope.command = {"cmd":"start", "output":"RUNNING..."};
        commandService.save($scope.command, function(command) {
            $scope.command = command;
            statusService.query({}, function(result) {
                $scope.status = result.status;
            });
        });
    };
}]);

app.controller('homeCtrl', ['$scope', 'unitService', function($scope, unitService) {
    $scope.groupedunits={};
    
    unitService.query({}, function(units) {
        for (unit of units) {
            if (! $scope.groupedunits.hasOwnProperty(unit.grouptag))
                $scope.groupedunits[unit.grouptag] = [];
            $scope.groupedunits[unit.grouptag].push(unit);
        }
    });
    
    $scope.toggle = function(unit) {
        unitService.save(unit, function(result) {
            Object.assign(unit,result);
        });
    };
}]);

app.controller('unitsCtrl', ['$scope', 'unitService', 'settingService', function($scope, unitService, settingService) {
    $scope.housecode = settingService.get({id: "HOUSECODE"}, function(setting) {
        $scope.housecode = setting.val;
        $scope.units = unitService.query({housecode: $scope.housecode});
    });    
    
    $scope.filter = function() {
        $scope.units = unitService.query({housecode: $scope.housecode})
    }
    
    $scope.onUnit = function(unit) {
        unit,unitService.save({id:unit.id, on:true}, function(result) {
            Object.assign(unit, result);
        });
    }
    $scope.offUnit = function(unit) {
        unit,unitService.save({id:unit.id, on:false}, function(result) {
            Object.assign(unit, result);
        });
    }
    $scope.configUnit = function(unit) {
        unit,unitService.config(unit, function(result) {
            Object.assign(unit, result);
        });
    }
}]);

app.controller('settingsCtrl', ['$scope', 'settingService', 'commandService', function($scope, settingService, commandService) {
    $scope.settings = settingService.query();

    $scope.change = function(setting) {
        settingService.save(setting, function(result) {
            Object.assign(setting, result);
        });
    };
    $scope.restart = function() {
        $scope.command = {"cmd":"restart", "output":"RUNNING..."};
        commandService.save($scope.command, function(command) {
            $scope.command = command;
        });
    };

    $scope.start = function() {
        $scope.command = {"cmd":"start", "output":"RUNNING..."};
        commandService.save($scope.command, function(command) {
            $scope.command = command;
        });
    };

    $scope.stop = function() {
        $scope.command = {"cmd":"stop", "output":"RUNNING..."};
        commandService.save($scope.command, function(command) {
            $scope.command = command;
        });
    };
}]);

app.controller('aliasesCtrl', ['$scope', '$route', '$mdDialog', 'aliasService', function($scope, $route, $mdDialog, aliasService) {
    $scope.groupedaliases={};

    aliasService.query({}, function(aliases) {
        for (alias of aliases) {
            if (! $scope.groupedaliases.hasOwnProperty(alias.grouptag))
                $scope.groupedaliases[alias.grouptag] = [];
            $scope.groupedaliases[alias.grouptag].push(alias);
        }        
    });
    
    $scope.editAlias = function(alias, forCreation) {
        $mdDialog.show({
            templateUrl: 'web/js/aliasDialog.html',
            controller: 'editDialogCtrl',
            clickOutsideToClose:true,
            locals:{'dialData':{'origItem': alias, 'forCreation': forCreation}},
        }).then(
            function(dialData) {
                    aliasService.save(dialData.editItem, function() {
                        $route.reload();
                    });
            }
        );
    };
    
    $scope.delAlias = function(alias) {
        var confirm = $mdDialog.confirm()
          .title('Delete Alias')
          .textContent('Delete ' + alias.id + '?')
          .ok('OK')
          .cancel('CANCEL');

        $mdDialog.show(confirm).then(function() {
            aliasService.delete(alias, function() {
                $route.reload();
            });
        });
    };
    
}]);

app.controller('schedulesCtrl', ['$scope', '$mdDialog', 'scheduleService', 'macroService', 'commandService', function($scope, $mdDialog, scheduleService, macroService, commandService) {
    $scope.schedules = scheduleService.query();
    $scope.scheduleLines = scheduleService.query({file:"true"});
    $scope.macros = macroService.query();
    
    $scope.upload = function() {
        $scope.command = {"cmd":"upload", "output":"RUNNING..."};
        commandService.save($scope.command, function(command) {
            $scope.command = command;
        });
    };
    $scope.reset = function() {
        $scope.command = {"cmd":"reset", "output":"RUNNING..."};
        commandService.save($scope.command, function(command) {
            $scope.command = command;
        });
    };

    $scope.editMacro = function(macro, forCreation) {
        $mdDialog.show({
            templateUrl: 'web/js/macroDialog.html',
            controller: 'editDialogCtrl',
            clickOutsideToClose:true,
            locals:{'dialData':{'origItem': macro, 'forCreation': forCreation}},
        }).then(
            function(dialData) {
                    macroService.save(dialData.editItem, function() {
                        $scope.macros = macroService.query();       
                    });
            }
        );
    };
    
    $scope.delMacro = function(macro) {
        var confirm = $mdDialog.confirm()
          .title('Delete Macro')
          .textContent('Delete ' + macro.id + '?')
          .ok('OK')
          .cancel('CANCEL');

        $mdDialog.show(confirm).then(function() {
            macroService.delete(macro, function() {
                $scope.macros = macroService.query(); 
            });
        });
    };

    $scope.toggleSchedule = function(schedule) {
        scheduleService.save(schedule, function() {
            $scope.schedules = scheduleService.query();       
        });
    };
    
    $scope.editSchedule = function(schedule, forCreation) {
        $mdDialog.show({
            templateUrl: 'web/js/scheduleDialog.html',
            controller: 'editDialogCtrl',
            clickOutsideToClose:true,
            locals:{'dialData':{'origItem': schedule, 'forCreation': forCreation, 'macros': $scope.macros}},
        }).then(
            function(dialData) {
                    scheduleService.save(dialData.editItem, function() {
                        $scope.schedules = scheduleService.query();       
                    });
            }
        );
    };
    
    $scope.delSchedule = function(schedule) {
        var confirm = $mdDialog.confirm()
          .title('Delete Schedule')
          .textContent('Delete ' + schedule.id + '?')
          .ok('OK')
          .cancel('CANCEL');

        $mdDialog.show(confirm).then(function() {
            scheduleService.delete(schedule, function() {
                $scope.schedules = scheduleService.query(); 
            });
        });
    };
}]);

app.controller('commandsCtrl', ['$scope', 'commandService', function($scope, commandService) {
    $scope.command = commandService.query();
    
    $scope.execute = function(cmd) {
        commandService.save({"cmd":cmd}, function(command) {
            $scope.command = command;
        });
    };
}]);

app.controller('editDialogCtrl', ['$scope', '$mdDialog', 'dialData', function ($scope, $mdDialog, dialData) {
    // important to have the copied item.
    $scope.dialData = dialData;
    $scope.dialData.editItem = angular.copy(dialData.origItem);
    if (dialData.forCreation && dialData.origItem) $scope.dialData.editItem.id = $scope.dialData.editItem.id + "_COPY"
    $scope.editOK = function(dialData) {
      $mdDialog.hide(dialData);
    }
    $scope.editCANCEL = function(dialData) {
      $mdDialog.cancel(dialData);
    };
    $scope.range = function(min, max, step) {
        if (max == undefined) {
            max = min;
            min = 0;
        }
        step = Math.abs(step) || 1;
        if (min > max) {
            step = -step;
        }
        var output = [];
        for (var value=min; value<max; value+=step) {
            output.push(value);
        }
        return output;
    };
}]);
