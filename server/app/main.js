(self["webpackChunkkinect_theia_console"] = self["webpackChunkkinect_theia_console"] || []).push([["main"],{

/***/ 3966:
/*!***************************************!*\
  !*** ./src/app/app-routing.module.ts ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AppRoutingModule: () => (/* binding */ AppRoutingModule)
/* harmony export */ });
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/router */ 7947);
/* harmony import */ var _components_architecture_architecture_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./components/architecture/architecture.component */ 7433);
/* harmony import */ var _components_dynamic_action_dynamic_action_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./components/dynamic-action/dynamic-action.component */ 334);
/* harmony import */ var _components_dynamic_section_dynamic_section_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./components/dynamic-section/dynamic-section.component */ 1954);
/* harmony import */ var _components_home_home_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./components/home/home.component */ 159);
/* harmony import */ var _components_readme_readme_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/readme/readme.component */ 7350);
/* harmony import */ var _components_not_found_not_found_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./components/not-found/not-found.component */ 6218);
/* harmony import */ var _services_environment_resolver__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./services/environment.resolver */ 3807);
/* harmony import */ var _services_template_resolver__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./services/template.resolver */ 908);
/* harmony import */ var _auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @auth0/auth0-angular */ 6742);
/* harmony import */ var _components_auth_error_auth_error_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components/auth-error/auth-error.component */ 6410);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/core */ 1699);













const routes = [{
  path: '',
  redirectTo: 'home',
  pathMatch: 'full'
}, {
  path: 'action',
  redirectTo: 'action/',
  pathMatch: 'full'
}, {
  path: 'architecture',
  component: _components_architecture_architecture_component__WEBPACK_IMPORTED_MODULE_0__.ArchitectureComponent,
  canActivate: [_auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_1__.AuthGuard],
  resolve: {
    template: _services_template_resolver__WEBPACK_IMPORTED_MODULE_2__.templateResolver,
    env: _services_environment_resolver__WEBPACK_IMPORTED_MODULE_3__.environmentResolver
  }
}, {
  path: 'home',
  component: _components_home_home_component__WEBPACK_IMPORTED_MODULE_4__.HomeComponent,
  canActivate: [_auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_1__.AuthGuard],
  resolve: {
    template: _services_template_resolver__WEBPACK_IMPORTED_MODULE_2__.templateResolver,
    env: _services_environment_resolver__WEBPACK_IMPORTED_MODULE_3__.environmentResolver
  }
}, {
  path: 'readme',
  component: _components_readme_readme_component__WEBPACK_IMPORTED_MODULE_5__.ReadmeComponent,
  canActivate: [_auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_1__.AuthGuard],
  resolve: {
    template: _services_template_resolver__WEBPACK_IMPORTED_MODULE_2__.templateResolver,
    env: _services_environment_resolver__WEBPACK_IMPORTED_MODULE_3__.environmentResolver
  }
}, {
  path: 'auth-error',
  component: _components_auth_error_auth_error_component__WEBPACK_IMPORTED_MODULE_6__.AuthErrorComponent
}, {
  path: 'action/:route',
  component: _components_dynamic_section_dynamic_section_component__WEBPACK_IMPORTED_MODULE_7__.DynamicSectionComponent,
  canActivate: [_auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_1__.AuthGuard],
  resolve: {
    template: _services_template_resolver__WEBPACK_IMPORTED_MODULE_2__.templateResolver,
    env: _services_environment_resolver__WEBPACK_IMPORTED_MODULE_3__.environmentResolver
  }
}, {
  path: 'action/:route/:action',
  component: _components_dynamic_action_dynamic_action_component__WEBPACK_IMPORTED_MODULE_8__.DynamicActionComponent,
  canActivate: [_auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_1__.AuthGuard],
  resolve: {
    template: _services_template_resolver__WEBPACK_IMPORTED_MODULE_2__.templateResolver,
    env: _services_environment_resolver__WEBPACK_IMPORTED_MODULE_3__.environmentResolver
  }
}, {
  path: '**',
  component: _components_not_found_not_found_component__WEBPACK_IMPORTED_MODULE_9__.NotFoundComponent
}];
let AppRoutingModule = /*#__PURE__*/(() => {
  class AppRoutingModule {
    static #_ = this.ɵfac = function AppRoutingModule_Factory(t) {
      return new (t || AppRoutingModule)();
    };
    static #_2 = this.ɵmod = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_10__["ɵɵdefineNgModule"]({
      type: AppRoutingModule
    });
    static #_3 = this.ɵinj = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_10__["ɵɵdefineInjector"]({
      imports: [_angular_router__WEBPACK_IMPORTED_MODULE_11__.RouterModule.forRoot(routes), _angular_router__WEBPACK_IMPORTED_MODULE_11__.RouterModule]
    });
  }
  return AppRoutingModule;
})();
(function () {
  (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_10__["ɵɵsetNgModuleScope"](AppRoutingModule, {
    imports: [_angular_router__WEBPACK_IMPORTED_MODULE_11__.RouterModule],
    exports: [_angular_router__WEBPACK_IMPORTED_MODULE_11__.RouterModule]
  });
})();

/***/ }),

/***/ 6401:
/*!**********************************!*\
  !*** ./src/app/app.component.ts ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AppComponent: () => (/* binding */ AppComponent)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ 8071);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ 5357);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ 3317);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ 25);
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../environments/environment */ 553);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_template_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./services/template.service */ 529);
/* harmony import */ var _services_cloud_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./services/cloud.service */ 9509);
/* harmony import */ var _services_allowed_apps_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./services/allowed-apps.service */ 9726);
/* harmony import */ var _auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @auth0/auth0-angular */ 6742);
/* harmony import */ var _services_environment_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./services/environment.service */ 1574);
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/router */ 7947);
/* harmony import */ var _services_window_ref_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./services/window-ref.service */ 6889);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _components_error_error_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./components/error/error.component */ 9426);













function AppComponent_ng_container_0_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](1, "div", 1)(2, "span", 2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](3, "Loading...");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
}
function AppComponent_ng_container_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](1, "router-outlet");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
}
function AppComponent_ng_container_5_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](1, "theia-error", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
}
let AppComponent = /*#__PURE__*/(() => {
  class AppComponent {
    constructor(templateService, cloud, app, authService, environment, router, windowRef) {
      this.templateService = templateService;
      this.cloud = cloud;
      this.app = app;
      this.authService = authService;
      this.environment = environment;
      this.router = router;
      this.windowRef = windowRef;
      this.environments$ = new rxjs__WEBPACK_IMPORTED_MODULE_2__.BehaviorSubject(undefined);
      this.template$ = templateService.template$;
      this.error = authService.error$;
      this.window = windowRef.nativeWindow;
      this.environments$ = environment.environments$;
    }
    ngOnInit() {
      const appChanged = this.app.getSelectedApp().pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_3__.skip)(1), (0,rxjs_operators__WEBPACK_IMPORTED_MODULE_4__.distinctUntilChanged)());
      this.app.getAllowedApps();
      this.cloud.getClouds().pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_5__.switchMapTo)(this.app.getAllowedApps()), (0,rxjs_operators__WEBPACK_IMPORTED_MODULE_5__.switchMapTo)(appChanged)).subscribe(() => {
        this.window.location.href = _environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.redirectUri;
      });
    }
    static #_ = this.ɵfac = function AppComponent_Factory(t) {
      return new (t || AppComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_template_service__WEBPACK_IMPORTED_MODULE_6__.TemplateService), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_cloud_service__WEBPACK_IMPORTED_MODULE_7__.CloudService), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_allowed_apps_service__WEBPACK_IMPORTED_MODULE_8__.AllowedAppsService), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_9__.AuthService), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_environment_service__WEBPACK_IMPORTED_MODULE_10__.EnvironmentService), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_angular_router__WEBPACK_IMPORTED_MODULE_11__.Router), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_window_ref_service__WEBPACK_IMPORTED_MODULE_12__.WindowRefService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineComponent"]({
      type: AppComponent,
      selectors: [["theia-root"]],
      decls: 7,
      vars: 11,
      consts: [[4, "ngIf"], ["role", "status", 1, "spinner-border", "spinner-big", "m-4", "text-primary", 2, "position", "absolute", "top", "calc(50% - 3rem)", "left", "calc(50% - 3rem)"], [1, "visually-hidden"], ["description", "", "error", "An error occurred", "header", "OOps!"]],
      template: function AppComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](0, AppComponent_ng_container_0_Template, 4, 0, "ng-container", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipe"](1, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipe"](2, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](3, AppComponent_ng_container_3_Template, 2, 0, "ng-container", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipe"](4, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](5, AppComponent_ng_container_5_Template, 2, 0, "ng-container", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipe"](6, "async");
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipeBind1"](1, 3, ctx.template$) === undefined || _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipeBind1"](2, 5, ctx.environments$) === undefined);
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](3);
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipeBind1"](4, 7, ctx.template$) !== null);
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipeBind1"](6, 9, ctx.template$) === null);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_13__.NgIf, _angular_router__WEBPACK_IMPORTED_MODULE_11__.RouterOutlet, _components_error_error_component__WEBPACK_IMPORTED_MODULE_14__.ErrorComponent, _angular_common__WEBPACK_IMPORTED_MODULE_13__.AsyncPipe],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return AppComponent;
})();

/***/ }),

/***/ 8629:
/*!*******************************!*\
  !*** ./src/app/app.module.ts ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AppModule: () => (/* binding */ AppModule)
/* harmony export */ });
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ 4860);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/forms */ 8849);
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/platform-browser */ 6480);
/* harmony import */ var _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @ng-select/ng-select */ 1788);
/* harmony import */ var ngx_markdown__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ngx-markdown */ 1995);
/* harmony import */ var _app_routing_module__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./app-routing.module */ 3966);
/* harmony import */ var _app_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./app.component */ 6401);
/* harmony import */ var _components_actions_actions_component__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./components/actions/actions.component */ 3494);
/* harmony import */ var _components_architecture_wizard_architecture_wizard_component__WEBPACK_IMPORTED_MODULE_34__ = __webpack_require__(/*! ./components/architecture-wizard/architecture-wizard.component */ 7204);
/* harmony import */ var _components_architecture_architecture_component__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./components/architecture/architecture.component */ 7433);
/* harmony import */ var _components_confirm_modal_confirm_modal_component__WEBPACK_IMPORTED_MODULE_27__ = __webpack_require__(/*! ./components/confirm-modal/confirm-modal.component */ 6530);
/* harmony import */ var _components_diagram_diagram_component__WEBPACK_IMPORTED_MODULE_35__ = __webpack_require__(/*! ./components/diagram/diagram.component */ 7254);
/* harmony import */ var _components_dynamic_action_dynamic_action_component__WEBPACK_IMPORTED_MODULE_37__ = __webpack_require__(/*! ./components/dynamic-action/dynamic-action.component */ 334);
/* harmony import */ var _components_dynamic_control_dynamic_control_component__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ./components/dynamic-control/dynamic-control.component */ 1081);
/* harmony import */ var _components_dynamic_form_dynamic_form_component__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ./components/dynamic-form/dynamic-form.component */ 3439);
/* harmony import */ var _components_dynamic_section_dynamic_section_component__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./components/dynamic-section/dynamic-section.component */ 1954);
/* harmony import */ var _components_error_error_component__WEBPACK_IMPORTED_MODULE_30__ = __webpack_require__(/*! ./components/error/error.component */ 9426);
/* harmony import */ var _components_footer_footer_component__WEBPACK_IMPORTED_MODULE_29__ = __webpack_require__(/*! ./components/footer/footer.component */ 7913);
/* harmony import */ var _components_grid_grid_component__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! ./components/grid/grid.component */ 3150);
/* harmony import */ var _components_header_header_component__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./components/header/header.component */ 6471);
/* harmony import */ var _components_home_home_component__WEBPACK_IMPORTED_MODULE_38__ = __webpack_require__(/*! ./components/home/home.component */ 159);
/* harmony import */ var _components_readme_readme_component__WEBPACK_IMPORTED_MODULE_39__ = __webpack_require__(/*! ./components/readme/readme.component */ 7350);
/* harmony import */ var _components_layout_layout_component__WEBPACK_IMPORTED_MODULE_32__ = __webpack_require__(/*! ./components/layout/layout.component */ 2952);
/* harmony import */ var _components_modal_modal_component__WEBPACK_IMPORTED_MODULE_28__ = __webpack_require__(/*! ./components/modal/modal.component */ 354);
/* harmony import */ var _components_not_found_not_found_component__WEBPACK_IMPORTED_MODULE_31__ = __webpack_require__(/*! ./components/not-found/not-found.component */ 6218);
/* harmony import */ var _components_sidebar_sidebar_component__WEBPACK_IMPORTED_MODULE_36__ = __webpack_require__(/*! ./components/sidebar/sidebar.component */ 7954);
/* harmony import */ var _components_steps_steps_component__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! ./components/steps/steps.component */ 5770);
/* harmony import */ var _components_tab_bar_tab_bar_component__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./components/tab-bar/tab-bar.component */ 7354);
/* harmony import */ var _directives_control_attributes_directive__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./directives/control-attributes.directive */ 2432);
/* harmony import */ var _directives_dropdown_directive__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! ./directives/dropdown.directive */ 1501);
/* harmony import */ var _pipes_remove_null_pipe__WEBPACK_IMPORTED_MODULE_33__ = __webpack_require__(/*! ./pipes/remove-null.pipe */ 8475);
/* harmony import */ var _components_info_info_component__WEBPACK_IMPORTED_MODULE_40__ = __webpack_require__(/*! ./components/info/info.component */ 3636);
/* harmony import */ var _components_key_value_editor_key_value_editor_component__WEBPACK_IMPORTED_MODULE_41__ = __webpack_require__(/*! ./components/key-value-editor/key-value-editor.component */ 1052);
/* harmony import */ var _auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @auth0/auth0-angular */ 6742);
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../environments/environment */ 553);
/* harmony import */ var _components_auth_error_auth_error_component__WEBPACK_IMPORTED_MODULE_42__ = __webpack_require__(/*! ./components/auth-error/auth-error.component */ 6410);
/* harmony import */ var _directives_submenu_directive__WEBPACK_IMPORTED_MODULE_43__ = __webpack_require__(/*! ./directives/submenu.directive */ 8520);
/* harmony import */ var _components_accordion_accordion_module__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./components/accordion/accordion.module */ 7062);
/* harmony import */ var _interceptors_cloud_interceptor__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./interceptors/cloud.interceptor */ 2985);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _directives_static_action_directive__WEBPACK_IMPORTED_MODULE_44__ = __webpack_require__(/*! ./directives/static-action.directive */ 7637);
/* harmony import */ var ng2_file_upload__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ng2-file-upload */ 8079);
/* harmony import */ var _pipes_file_size_pipe__WEBPACK_IMPORTED_MODULE_45__ = __webpack_require__(/*! ./pipes/file-size.pipe */ 77);
/* harmony import */ var _components_dashboard_dashboard_module__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./components/dashboard/dashboard.module */ 1010);
/* harmony import */ var _interceptors_template_reload_interceptor__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./interceptors/template-reload.interceptor */ 1649);
/* harmony import */ var _components_pagination_pagination_component__WEBPACK_IMPORTED_MODULE_46__ = __webpack_require__(/*! ./components/pagination/pagination.component */ 2649);
/* harmony import */ var _components_type_ahead_type_ahead_component__WEBPACK_IMPORTED_MODULE_47__ = __webpack_require__(/*! ./components/type-ahead/type-ahead.component */ 3858);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_51__ = __webpack_require__(/*! rxjs/operators */ 1527);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_52__ = __webpack_require__(/*! rxjs/operators */ 3738);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_53__ = __webpack_require__(/*! rxjs/operators */ 2389);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_54__ = __webpack_require__(/*! rxjs */ 4980);
/* harmony import */ var _components_composite_group_composite_group_component__WEBPACK_IMPORTED_MODULE_48__ = __webpack_require__(/*! ./components/composite-group/composite-group.component */ 2096);
/* harmony import */ var _directives_resize_observer_directive__WEBPACK_IMPORTED_MODULE_49__ = __webpack_require__(/*! ./directives/resize-observer.directive */ 5067);
/* harmony import */ var _directives_log_stream_directive__WEBPACK_IMPORTED_MODULE_50__ = __webpack_require__(/*! ./directives/log-stream.directive */ 30);
























































let AppModule = /*#__PURE__*/(() => {
  class AppModule {
    static #_ = this.ɵfac = function AppModule_Factory(t) {
      return new (t || AppModule)();
    };
    static #_2 = this.ɵmod = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineNgModule"]({
      type: AppModule,
      bootstrap: [_app_component__WEBPACK_IMPORTED_MODULE_2__.AppComponent]
    });
    static #_3 = this.ɵinj = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineInjector"]({
      providers: [{
        provide: _angular_core__WEBPACK_IMPORTED_MODULE_1__.APP_INITIALIZER,
        useFactory: initializeAppFactory,
        deps: [_auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_3__.AuthService],
        multi: true
      }, {
        provide: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__.HTTP_INTERCEPTORS,
        useClass: _auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_3__.AuthHttpInterceptor,
        multi: true
      }, {
        provide: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__.HTTP_INTERCEPTORS,
        useClass: _interceptors_cloud_interceptor__WEBPACK_IMPORTED_MODULE_5__.CloudInterceptor,
        multi: true
      }, {
        provide: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__.HTTP_INTERCEPTORS,
        useClass: _interceptors_template_reload_interceptor__WEBPACK_IMPORTED_MODULE_6__.TemplateReloadInterceptor,
        multi: true
      }, {
        provide: _angular_common__WEBPACK_IMPORTED_MODULE_7__.APP_BASE_HREF,
        useValue: _environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.baseHref
      }],
      imports: [_angular_platform_browser__WEBPACK_IMPORTED_MODULE_8__.BrowserModule, _app_routing_module__WEBPACK_IMPORTED_MODULE_9__.AppRoutingModule, _angular_common_http__WEBPACK_IMPORTED_MODULE_4__.HttpClientModule, _angular_forms__WEBPACK_IMPORTED_MODULE_10__.FormsModule, _angular_forms__WEBPACK_IMPORTED_MODULE_10__.ReactiveFormsModule, ngx_markdown__WEBPACK_IMPORTED_MODULE_11__.MarkdownModule.forRoot(), _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_12__.NgSelectModule, _auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_3__.AuthModule.forRoot({
        ..._environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.auth0,
        errorPath: '/auth-error',
        authorizationParams: {
          redirect_uri: window.location.origin + _environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.redirectUri,
          ..._environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.authorizationParams
        },
        httpInterceptor: {
          allowedList: [{
            uri: '*',
            allowAnonymous: true
          }]
        }
      }), _components_accordion_accordion_module__WEBPACK_IMPORTED_MODULE_13__.AccordionModule, ng2_file_upload__WEBPACK_IMPORTED_MODULE_14__.FileUploadModule, _components_dashboard_dashboard_module__WEBPACK_IMPORTED_MODULE_15__.DashboardModule]
    });
  }
  return AppModule;
})();
(function () {
  (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵsetNgModuleScope"](AppModule, {
    declarations: [_app_component__WEBPACK_IMPORTED_MODULE_2__.AppComponent, _components_header_header_component__WEBPACK_IMPORTED_MODULE_16__.HeaderComponent, _components_tab_bar_tab_bar_component__WEBPACK_IMPORTED_MODULE_17__.TabBarComponent, _components_actions_actions_component__WEBPACK_IMPORTED_MODULE_18__.ActionsComponent, _components_architecture_architecture_component__WEBPACK_IMPORTED_MODULE_19__.ArchitectureComponent, _components_dynamic_section_dynamic_section_component__WEBPACK_IMPORTED_MODULE_20__.DynamicSectionComponent, _components_dynamic_control_dynamic_control_component__WEBPACK_IMPORTED_MODULE_21__.DynamicControlComponent, _directives_control_attributes_directive__WEBPACK_IMPORTED_MODULE_22__.ControlAttributesDirective, _components_dynamic_form_dynamic_form_component__WEBPACK_IMPORTED_MODULE_23__.DynamicFormComponent, _components_steps_steps_component__WEBPACK_IMPORTED_MODULE_24__.StepsComponent, _components_grid_grid_component__WEBPACK_IMPORTED_MODULE_25__.GridComponent, _directives_dropdown_directive__WEBPACK_IMPORTED_MODULE_26__.DropdownDirective, _components_confirm_modal_confirm_modal_component__WEBPACK_IMPORTED_MODULE_27__.ConfirmModalComponent, _components_modal_modal_component__WEBPACK_IMPORTED_MODULE_28__.ModalComponent, _components_footer_footer_component__WEBPACK_IMPORTED_MODULE_29__.FooterComponent, _components_error_error_component__WEBPACK_IMPORTED_MODULE_30__.ErrorComponent, _components_not_found_not_found_component__WEBPACK_IMPORTED_MODULE_31__.NotFoundComponent, _components_layout_layout_component__WEBPACK_IMPORTED_MODULE_32__.LayoutComponent, _pipes_remove_null_pipe__WEBPACK_IMPORTED_MODULE_33__.RemoveNullPipe, _components_architecture_wizard_architecture_wizard_component__WEBPACK_IMPORTED_MODULE_34__.ArchitectureWizardComponent, _components_diagram_diagram_component__WEBPACK_IMPORTED_MODULE_35__.DiagramComponent, _components_sidebar_sidebar_component__WEBPACK_IMPORTED_MODULE_36__.SidebarComponent, _components_dynamic_action_dynamic_action_component__WEBPACK_IMPORTED_MODULE_37__.DynamicActionComponent, _components_home_home_component__WEBPACK_IMPORTED_MODULE_38__.HomeComponent, _components_readme_readme_component__WEBPACK_IMPORTED_MODULE_39__.ReadmeComponent, _components_info_info_component__WEBPACK_IMPORTED_MODULE_40__.InfoComponent, _components_key_value_editor_key_value_editor_component__WEBPACK_IMPORTED_MODULE_41__.KeyValueEditorComponent, _components_auth_error_auth_error_component__WEBPACK_IMPORTED_MODULE_42__.AuthErrorComponent, _directives_submenu_directive__WEBPACK_IMPORTED_MODULE_43__.SubmenuDirective, _directives_static_action_directive__WEBPACK_IMPORTED_MODULE_44__.StaticActionDirective, _pipes_file_size_pipe__WEBPACK_IMPORTED_MODULE_45__.FileSizePipe, _components_pagination_pagination_component__WEBPACK_IMPORTED_MODULE_46__.PaginationComponent, _components_type_ahead_type_ahead_component__WEBPACK_IMPORTED_MODULE_47__.TypeAheadComponent, _components_composite_group_composite_group_component__WEBPACK_IMPORTED_MODULE_48__.CompositeGroupComponent, _directives_resize_observer_directive__WEBPACK_IMPORTED_MODULE_49__.ResizeObserverDirective, _directives_log_stream_directive__WEBPACK_IMPORTED_MODULE_50__.LogStreamDirective],
    imports: [_angular_platform_browser__WEBPACK_IMPORTED_MODULE_8__.BrowserModule, _app_routing_module__WEBPACK_IMPORTED_MODULE_9__.AppRoutingModule, _angular_common_http__WEBPACK_IMPORTED_MODULE_4__.HttpClientModule, _angular_forms__WEBPACK_IMPORTED_MODULE_10__.FormsModule, _angular_forms__WEBPACK_IMPORTED_MODULE_10__.ReactiveFormsModule, ngx_markdown__WEBPACK_IMPORTED_MODULE_11__.MarkdownModule, _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_12__.NgSelectModule, _auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_3__.AuthModule, _components_accordion_accordion_module__WEBPACK_IMPORTED_MODULE_13__.AccordionModule, ng2_file_upload__WEBPACK_IMPORTED_MODULE_14__.FileUploadModule, _components_dashboard_dashboard_module__WEBPACK_IMPORTED_MODULE_15__.DashboardModule, _angular_common__WEBPACK_IMPORTED_MODULE_7__.NgOptimizedImage]
  });
})();
function initializeAppFactory(auth) {
  return () => auth.user$.pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_51__.take)(1), (0,rxjs_operators__WEBPACK_IMPORTED_MODULE_52__.tap)(user => {
    const appMetadata = user["https://rapid-cloud.io/app_metadata"];
    if (appMetadata?.host_url) {
      _environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl = appMetadata.host_url;
    }
  }), (0,rxjs_operators__WEBPACK_IMPORTED_MODULE_53__.catchError)(err => {
    return (0,rxjs__WEBPACK_IMPORTED_MODULE_54__.of)(err);
  }));
}

/***/ }),

/***/ 7062:
/*!**********************************************************!*\
  !*** ./src/app/components/accordion/accordion.module.ts ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AccordionModule: () => (/* binding */ AccordionModule)
/* harmony export */ });
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _components_accordion_accordion_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/accordion/accordion.component */ 1638);
/* harmony import */ var _components_accordion_item_accordion_item_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/accordion-item/accordion-item.component */ 2836);
/* harmony import */ var _directives_intersection_observer_directive__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./directives/intersection-observer.directive */ 3154);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);





let AccordionModule = /*#__PURE__*/(() => {
  class AccordionModule {
    static #_ = this.ɵfac = function AccordionModule_Factory(t) {
      return new (t || AccordionModule)();
    };
    static #_2 = this.ɵmod = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineNgModule"]({
      type: AccordionModule
    });
    static #_3 = this.ɵinj = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjector"]({
      imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__.CommonModule]
    });
  }
  return AccordionModule;
})();
(function () {
  (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsetNgModuleScope"](AccordionModule, {
    declarations: [_components_accordion_accordion_component__WEBPACK_IMPORTED_MODULE_2__.AccordionComponent, _components_accordion_item_accordion_item_component__WEBPACK_IMPORTED_MODULE_3__.AccordionItemComponent, _directives_intersection_observer_directive__WEBPACK_IMPORTED_MODULE_4__.IntersectionObserverDirective],
    imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__.CommonModule],
    exports: [_components_accordion_accordion_component__WEBPACK_IMPORTED_MODULE_2__.AccordionComponent, _components_accordion_item_accordion_item_component__WEBPACK_IMPORTED_MODULE_3__.AccordionItemComponent]
  });
})();

/***/ }),

/***/ 2836:
/*!********************************************************************************************!*\
  !*** ./src/app/components/accordion/components/accordion-item/accordion-item.component.ts ***!
  \********************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AccordionItemComponent: () => (/* binding */ AccordionItemComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _directives_intersection_observer_directive__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../directives/intersection-observer.directive */ 3154);



const _c0 = ["accordionHeader"];
const _c1 = ["accordionControl"];
const _c2 = ["template"];
const _c3 = ["accordionTop"];
function AccordionItemComponent_ng_template_0_Template(rf, ctx) {
  if (rf & 1) {
    const _r4 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 1, 2)(2, "h2", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("visible", function AccordionItemComponent_ng_template_0_Template_h2_visible_2_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r4);
      const ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r3.onVisible($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "div", 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function AccordionItemComponent_ng_template_0_Template_div_click_3_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r4);
      const ctx_r5 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r5.toggleItem($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵprojection"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "div", 5)(6, "div", 6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵprojection"](7, 1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
  }
  if (rf & 2) {
    const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵclassProp"]("collapsed", ctx_r1.collapsed);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵclassProp"]("show", !ctx_r1.collapsed);
  }
}
const _c4 = [[["", "slot", "header"]], [["", "slot", "body"]]];
const _c5 = ["[slot=header]", "[slot=body]"];
let AccordionItemComponent = /*#__PURE__*/(() => {
  class AccordionItemComponent {
    constructor(viewContainerRef) {
      this.viewContainerRef = viewContainerRef;
      this.collapsed = true;
      this.visible = false;
      this.collapsing = false;
      this.collapse = new _angular_core__WEBPACK_IMPORTED_MODULE_0__.EventEmitter();
      this.expand = new _angular_core__WEBPACK_IMPORTED_MODULE_0__.EventEmitter();
    }
    ngOnInit() {
      this.viewContainerRef.createEmbeddedView(this.template);
    }
    toggleItem(event) {
      event.stopPropagation();
      this.collapsed = !this.collapsed;
      if (this.collapsed) {
        this.collapse.emit();
      } else {
        this.expand.emit();
        setTimeout(() => {
          this.top.nativeElement.scrollIntoView({
            behavior: "smooth"
          });
        }, 0);
      }
    }
    setChildrenReadOnly(readOnly) {
      this.children?.forEach(item => {
        if (readOnly) {
          item.ngControl.control?.disable({
            emitEvent: false,
            onlySelf: true
          });
        } else {
          item.ngControl.control?.enable({
            emitEvent: false,
            onlySelf: true
          });
        }
      });
    }
    ngAfterViewInit() {
      setTimeout(() => {
        this.setChildrenReadOnly(!this.header?.value);
      });
    }
    onVisible(visible) {
      this.visible = visible;
    }
    static #_ = this.ɵfac = function AccordionItemComponent_Factory(t) {
      return new (t || AccordionItemComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.ViewContainerRef));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: AccordionItemComponent,
      selectors: [["theia-accordion-item"]],
      contentQueries: function AccordionItemComponent_ContentQueries(rf, ctx, dirIndex) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵcontentQuery"](dirIndex, _c0, 5);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵcontentQuery"](dirIndex, _c1, 4);
        }
        if (rf & 2) {
          let _t;
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.header = _t.first);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.children = _t);
        }
      },
      viewQuery: function AccordionItemComponent_Query(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵviewQuery"](_c2, 7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵviewQuery"](_c3, 5);
        }
        if (rf & 2) {
          let _t;
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.template = _t.first);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.top = _t.first);
        }
      },
      outputs: {
        collapse: "collapse",
        expand: "expand"
      },
      ngContentSelectors: _c5,
      decls: 2,
      vars: 0,
      consts: [["template", ""], [1, "accordion-item"], ["accordionTop", ""], ["theiaIntersectionObserver", "", 1, "accordion-header", 3, "visible"], [1, "accordion-button", 3, "click"], [1, "accordion-collapse", "collapse"], [1, "accordion-body"]],
      template: function AccordionItemComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵprojectionDef"](_c4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](0, AccordionItemComponent_ng_template_0_Template, 8, 4, "ng-template", null, 0, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplateRefExtractor"]);
        }
      },
      dependencies: [_directives_intersection_observer_directive__WEBPACK_IMPORTED_MODULE_1__.IntersectionObserverDirective],
      styles: [".accordion-button[_ngcontent-%COMP%] {\n  cursor: pointer;\n}\n\n.accordion-button[_ngcontent-%COMP%]     .form-check-label {\n  margin-top: 0.2rem;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9hY2NvcmRpb24vY29tcG9uZW50cy9hY2NvcmRpb24taXRlbS9hY2NvcmRpb24taXRlbS5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLGVBQUE7QUFDRjs7QUFFQTtFQUNFLGtCQUFBO0FBQ0YiLCJzb3VyY2VzQ29udGVudCI6WyIuYWNjb3JkaW9uLWJ1dHRvbiB7XG4gIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuLmFjY29yZGlvbi1idXR0b24gOjpuZy1kZWVwIC5mb3JtLWNoZWNrLWxhYmVsIHtcbiAgbWFyZ2luLXRvcDogMC4ycmVtO1xufVxuIl0sInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return AccordionItemComponent;
})();

/***/ }),

/***/ 1638:
/*!**********************************************************************************!*\
  !*** ./src/app/components/accordion/components/accordion/accordion.component.ts ***!
  \**********************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AccordionComponent: () => (/* binding */ AccordionComponent)
/* harmony export */ });
/* harmony import */ var _accordion_item_accordion_item_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../accordion-item/accordion-item.component */ 2836);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);


const _c0 = ["*"];
let AccordionComponent = /*#__PURE__*/(() => {
  class AccordionComponent {
    constructor() {}
    ngAfterViewInit() {
      this.items.forEach((item, index) => {
        item.header?.ngControl.valueChanges?.subscribe(value => {
          if (value) {
            this.handleExpand(index);
          } else {
            item.collapsed = true;
          }
          item.setChildrenReadOnly(!value);
        });
        item.expand.subscribe(() => {
          this.handleExpand(index);
        });
      });
    }
    handleExpand(expandedItem) {
      this.items.forEach((item, index) => {
        if (expandedItem !== index) {
          item.collapsed = true;
        }
      });
    }
    static #_ = this.ɵfac = function AccordionComponent_Factory(t) {
      return new (t || AccordionComponent)();
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: AccordionComponent,
      selectors: [["theia-accordion"]],
      contentQueries: function AccordionComponent_ContentQueries(rf, ctx, dirIndex) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵcontentQuery"](dirIndex, _accordion_item_accordion_item_component__WEBPACK_IMPORTED_MODULE_1__.AccordionItemComponent, 4);
        }
        if (rf & 2) {
          let _t;
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.items = _t);
        }
      },
      ngContentSelectors: _c0,
      decls: 2,
      vars: 0,
      consts: [[1, "accordion", "mb-3"]],
      template: function AccordionComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵprojectionDef"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵprojection"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }
      },
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return AccordionComponent;
})();

/***/ }),

/***/ 3154:
/*!************************************************************************************!*\
  !*** ./src/app/components/accordion/directives/intersection-observer.directive.ts ***!
  \************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IntersectionObserverDirective: () => (/* binding */ IntersectionObserverDirective)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ 2513);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ 4520);




let IntersectionObserverDirective = /*#__PURE__*/(() => {
  class IntersectionObserverDirective {
    constructor(element) {
      this.element = element;
      this.threshold = 1;
      this.visible = new _angular_core__WEBPACK_IMPORTED_MODULE_0__.EventEmitter();
      this.subject$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.Subject();
    }
    ngOnInit() {
      this.createObserver();
    }
    ngAfterViewInit() {
      this.startObservingElements();
    }
    ngOnDestroy() {
      if (this.observer) {
        this.observer.disconnect();
        this.observer = undefined;
      }
      this.subject$.next(false);
      this.subject$.complete();
    }
    createObserver() {
      const options = {
        rootMargin: '0px',
        threshold: this.threshold
      };
      const isIntersecting = entry => entry.isIntersecting || entry.intersectionRatio > 0;
      this.observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          this.subject$.next(isIntersecting(entry));
        });
      }, options);
    }
    startObservingElements() {
      if (!this.observer) {
        return;
      }
      this.observer.observe(this.element.nativeElement);
      this.subject$.pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_2__.filter)(data => data !== undefined)).subscribe(visible => {
        this.visible.emit(visible);
      });
    }
    static #_ = this.ɵfac = function IntersectionObserverDirective_Factory(t) {
      return new (t || IntersectionObserverDirective)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.ElementRef));
    };
    static #_2 = this.ɵdir = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineDirective"]({
      type: IntersectionObserverDirective,
      selectors: [["", "theiaIntersectionObserver", ""]],
      inputs: {
        threshold: "threshold"
      },
      outputs: {
        visible: "visible"
      }
    });
  }
  return IntersectionObserverDirective;
})();

/***/ }),

/***/ 3494:
/*!*********************************************************!*\
  !*** ./src/app/components/actions/actions.component.ts ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ActionsComponent: () => (/* binding */ ActionsComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ 6575);



const _c0 = function (a0) {
  return {
    active: a0
  };
};
function ActionsComponent_a_1_Template(rf, ctx) {
  if (rf & 1) {
    const _r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "a", 2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function ActionsComponent_a_1_Template_a_click_0_listener() {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r3);
      const action_r1 = restoredCtx.$implicit;
      const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r2.handleActionClick(action_r1));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const action_r1 = ctx.$implicit;
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](2, _c0, (action_r1 == null ? null : action_r1.id) === (ctx_r0.currentAction == null ? null : ctx_r0.currentAction.id)));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", action_r1 == null ? null : action_r1.label, " ");
  }
}
let ActionsComponent = /*#__PURE__*/(() => {
  class ActionsComponent {
    constructor() {
      this.actions = [];
      this.actionSelected = new _angular_core__WEBPACK_IMPORTED_MODULE_0__.EventEmitter();
    }
    handleActionClick(action) {
      this.currentAction = action;
      this.actionSelected.emit(action);
      return false;
    }
    static #_ = this.ɵfac = function ActionsComponent_Factory(t) {
      return new (t || ActionsComponent)();
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: ActionsComponent,
      selectors: [["theia-actions"]],
      inputs: {
        actions: "actions"
      },
      outputs: {
        actionSelected: "actionSelected"
      },
      decls: 2,
      vars: 1,
      consts: [[1, "list-group"], ["class", "list-group-item list-group-item-action", "href", "", 3, "ngClass", "click", 4, "ngFor", "ngForOf"], ["href", "", 1, "list-group-item", "list-group-item-action", 3, "ngClass", "click"]],
      template: function ActionsComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, ActionsComponent_a_1_Template, 2, 4, "a", 1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx.actions);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_1__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_1__.NgForOf],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return ActionsComponent;
})();

/***/ }),

/***/ 7204:
/*!*********************************************************************************!*\
  !*** ./src/app/components/architecture-wizard/architecture-wizard.component.ts ***!
  \*********************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ArchitectureWizardComponent: () => (/* binding */ ArchitectureWizardComponent)
/* harmony export */ });
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs/operators */ 1891);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_template_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../services/template.service */ 529);
/* harmony import */ var _services_command_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../services/command.service */ 9167);
/* harmony import */ var _services_log_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/log.service */ 2553);
/* harmony import */ var _services_environment_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/environment.service */ 1574);
/* harmony import */ var _services_info_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/info.service */ 957);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/forms */ 8849);
/* harmony import */ var _modal_modal_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../modal/modal.component */ 354);
/* harmony import */ var _diagram_diagram_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../diagram/diagram.component */ 7254);











const _c0 = function (a0, a1) {
  return {
    control: a0,
    id: a1
  };
};
function ArchitectureWizardComponent_ng_container_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainer"](1, 18);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const el_r5 = ctx.$implicit;
    const i_r6 = ctx.index;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    const _r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](11);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngTemplateOutletContext", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction2"](2, _c0, el_r5, i_r6))("ngTemplateOutlet", _r2);
  }
}
function ArchitectureWizardComponent_span_6_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "span", 19);
  }
}
function ArchitectureWizardComponent_ng_template_10_ng_container_7_ng_container_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainer"](1, 18);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const el_r11 = ctx.$implicit;
    const i_r12 = ctx.index;
    const id_r8 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2).id;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    const _r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](11);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngTemplateOutletContext", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction2"](2, _c0, el_r11, id_r8 + "_" + i_r12))("ngTemplateOutlet", _r2);
  }
}
function ArchitectureWizardComponent_ng_template_10_ng_container_7_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceHTML"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 27);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, ArchitectureWizardComponent_ng_template_10_ng_container_7_ng_container_2_Template, 2, 5, "ng-container", 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const control_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().control;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", control_r7.children);
  }
}
const _c1 = function (a0) {
  return {
    show: a0
  };
};
function ArchitectureWizardComponent_ng_template_10_Template(rf, ctx) {
  if (rf & 1) {
    const _r16 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 20)(1, "div", 21);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("mouseenter", function ArchitectureWizardComponent_ng_template_10_Template_div_mouseenter_1_listener() {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r16);
      const control_r7 = restoredCtx.control;
      const id_r8 = restoredCtx.id;
      const ctx_r15 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r15.onMouseEnter(control_r7, id_r8));
    })("mouseleave", function ArchitectureWizardComponent_ng_template_10_Template_div_mouseleave_1_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r16);
      const ctx_r17 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r17.onMouseLeave());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "input", 22);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("change", function ArchitectureWizardComponent_ng_template_10_Template_input_change_2_listener($event) {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r16);
      const control_r7 = restoredCtx.control;
      const ctx_r18 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r18.onOptionChange($event, control_r7));
    })("ngModelChange", function ArchitectureWizardComponent_ng_template_10_Template_input_ngModelChange_2_listener($event) {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r16);
      const control_r7 = restoredCtx.control;
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](control_r7.checked = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "label", 23);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "svg", 24);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function ArchitectureWizardComponent_ng_template_10_Template__svg_svg_click_5_listener() {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r16);
      const control_r7 = restoredCtx.control;
      const ctx_r20 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r20.showCommands(control_r7));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](6, "path", 25);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](7, ArchitectureWizardComponent_ng_template_10_ng_container_7_Template, 3, 1, "ng-container", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const control_r7 = ctx.control;
    const id_r8 = ctx.id;
    const ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngModel", control_r7.checked)("id", id_r8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("for", id_r8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](control_r7.text);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](6, _c1, id_r8 === ctx_r3.currentOption));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", control_r7.children && control_r7.children.length && control_r7.checked);
  }
}
function ArchitectureWizardComponent_div_39_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const command_r21 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", command_r21, " ");
  }
}
let ArchitectureWizardComponent = /*#__PURE__*/(() => {
  class ArchitectureWizardComponent {
    constructor(templateService, commandService, logService, environmentService, infoService) {
      this.templateService = templateService;
      this.commandService = commandService;
      this.logService = logService;
      this.environmentService = environmentService;
      this.infoService = infoService;
      this.options = [];
      this.diagram = {
        cellSize: 20,
        rows: 30,
        columns: 36,
        grid: false,
        icons: [],
        links: []
      };
      this.submitting = false;
      this.log = '';
      this.showLog = false;
      this.showError = false;
      this.currentOption = '';
      this.showCommandsModal = false;
      this.selectedCommands = [];
    }
    ngOnInit() {
      const match = (this.data?.id || '').match(/^(aws|azure|gcp)_([^_]+)_wizard$/);
      // const match = (this.data?.id || '').match(/^aws_([^_]+)_wizard$/);
      console.log(match);
      // OLD
      // 0: "aws_solution_wizard"
      // 1: "solution"
      //
      // NEW
      // 0: "aws_solution_wizard"
      // 1: "aws"
      // 2:"solution"    
      if (!match || !match.length) {
        return;
      }
      const endpoint = match[2];
      this.templateService.getDiagramData(`wizard/${endpoint}`, []).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_1__.switchMap)(data => {
        this.options = data;
        this.infoService.data = this.data?.info || '';
        return this.templateService.getDiagramData(this.data?.endpoint || '', this.diagram);
      })).subscribe(diagram => {
        diagram.icons = diagram.icons.map(icon => {
          icon.display = false;
          delete icon.active;
          return icon;
        });
        diagram.cellSize = 23;
        this.diagram = diagram;
        this.optionChanged();
      });
    }
    optionChanged() {
      const selectedIds = new Set();
      const highlightedActions = new Set();
      const getSelectedIs = options => {
        options.forEach(option => {
          if (option.checked) {
            option.ids.forEach(id => selectedIds.add(Number(id)));
            (option.actions || []).forEach(id => highlightedActions.add(id));
          }
          if (option.children?.length) {
            getSelectedIs(option.children);
          }
        });
      };
      getSelectedIs(this.options);
      this.diagram.icons.forEach(icon => {
        icon.display = [...selectedIds].includes(Number(icon.id));
      });
      this.environmentService.highlightedActions$.next([...highlightedActions]);
    }
    getIconById(id) {
      return this.diagram.icons.find(icon => Number(icon.id) === Number(id));
    }
    onOptionChange(event, option) {
      const target = event.currentTarget;
      if (!target.checked && option.children?.length) {
        this.disableChildren(option.children);
      }
      this.optionChanged();
    }
    disableChildren(options) {
      options.forEach(option => {
        option.checked = false;
        if (option.children?.length) {
          this.disableChildren(option.children);
        }
      });
    }
    sendPayload() {
      const payload = {
        ...this.data?.command.command,
        wizard: this.options
      };
      this.submitting = true;
      this.commandService.runCommand(payload).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_1__.switchMap)(resp => this.logService.getLog(resp.log_file))).subscribe(log => {
        this.log = log;
        this.showLog = true;
        this.submitting = false;
      }, () => {
        this.submitting = false;
        this.showError = true;
      });
    }
    modalClose() {
      this.showLog = false;
      this.showError = false;
    }
    showCommands(option) {
      this.showCommandsModal = true;
      this.selectedCommands = option.cli;
    }
    onMouseEnter(option, id) {
      if (!option.cli || !option.cli.length) {
        return;
      }
      this.currentOption = id;
    }
    onMouseLeave() {
      this.currentOption = '';
    }
    commandsModalClose() {
      this.showCommandsModal = false;
      this.selectedCommands = [];
    }
    static #_ = this.ɵfac = function ArchitectureWizardComponent_Factory(t) {
      return new (t || ArchitectureWizardComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_template_service__WEBPACK_IMPORTED_MODULE_2__.TemplateService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_command_service__WEBPACK_IMPORTED_MODULE_3__.CommandService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_log_service__WEBPACK_IMPORTED_MODULE_4__.LogService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_environment_service__WEBPACK_IMPORTED_MODULE_5__.EnvironmentService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_info_service__WEBPACK_IMPORTED_MODULE_6__.InfoService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: ArchitectureWizardComponent,
      selectors: [["theia-diagram-options"]],
      inputs: {
        data: "data"
      },
      decls: 43,
      vars: 10,
      consts: [[1, "card"], [1, "card-body"], [1, "d-flex", "justify-content-between"], [1, "overflow-auto", "wizard-options", "px-1"], [4, "ngFor", "ngForOf"], [1, "btn", "btn-primary", "mt-5", 3, "disabled", "click"], ["class", "spinner-border spinner-border-sm", 4, "ngIf"], [3, "diagram"], ["line", ""], ["classes", "modal-xl modal-dialog-scrollable modal-dialog-centered", 3, "visible"], ["slot", "header"], [1, "modal-title"], ["type", "button", "data-bs-dismiss", "modal", "aria-label", "Close", 1, "btn-close", 3, "click"], ["slot", "body"], ["slot", "footer"], ["type", "button", 1, "btn", "btn-primary", 3, "click"], ["classes", "modal-sm modal-dialog-centered", 3, "visible"], ["classes", "modal modal-dialog-scrollable modal-dialog-centered", 3, "visible"], [3, "ngTemplateOutletContext", "ngTemplateOutlet"], [1, "spinner-border", "spinner-border-sm"], [1, "wizard-option"], [1, "form-check", 3, "mouseenter", "mouseleave"], ["type", "checkbox", 1, "form-check-input", 3, "ngModel", "id", "change", "ngModelChange"], [1, "form-check-label", 3, "for"], ["xmlns", "http://www.w3.org/2000/svg", "width", "16", "height", "16", "fill", "currentColor", "viewBox", "0 0 16 16", 1, "bi", "bi-terminal-fill", "terminal", 3, "ngClass", "click"], ["d", "M0 3a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3zm9.5 5.5h-3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm-6.354-.354a.5.5 0 1 0 .708.708l2-2a.5.5 0 0 0 0-.708l-2-2a.5.5 0 1 0-.708.708L4.793 6.5 3.146 8.146z"], [4, "ngIf"], [2, "margin-left", "2rem"]],
      template: function ArchitectureWizardComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 0)(1, "div", 1)(2, "div", 2)(3, "div", 3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, ArchitectureWizardComponent_ng_container_4_Template, 2, 5, "ng-container", 4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "button", 5);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function ArchitectureWizardComponent_Template_button_click_5_listener() {
            return ctx.sendPayload();
          });
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](6, ArchitectureWizardComponent_span_6_Template, 1, 0, "span", 6);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](8, "div");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](9, "theia-diagram", 7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](10, ArchitectureWizardComponent_ng_template_10_Template, 8, 8, "ng-template", null, 8, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplateRefExtractor"]);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](12, "theia-modal", 9);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](13, 10);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](14, "h5", 11);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](15, "Log");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](16, "button", 12);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function ArchitectureWizardComponent_Template_button_click_16_listener() {
            return ctx.modalClose();
          });
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](17, 13);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](18, "pre");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](19);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](20, 14);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](21, "button", 15);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function ArchitectureWizardComponent_Template_button_click_21_listener() {
            return ctx.modalClose();
          });
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](22, "Ok");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](23, "theia-modal", 16);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](24, 10);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](25, "h5", 11);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](26, "Error");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](27, "button", 12);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function ArchitectureWizardComponent_Template_button_click_27_listener() {
            return ctx.modalClose();
          });
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](28, 13);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](29, " An error occurred please try again later ");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](30, 14);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](31, "button", 15);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function ArchitectureWizardComponent_Template_button_click_31_listener() {
            return ctx.modalClose();
          });
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](32, "Ok");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](33, "theia-modal", 17);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](34, 10);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](35, "h5", 11);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](36, "Commands");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](37, "button", 12);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function ArchitectureWizardComponent_Template_button_click_37_listener() {
            return ctx.commandsModalClose();
          });
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](38, 13);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](39, ArchitectureWizardComponent_div_39_Template, 2, 1, "div", 4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](40, 14);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](41, "button", 15);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function ArchitectureWizardComponent_Template_button_click_41_listener() {
            return ctx.commandsModalClose();
          });
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](42, "Ok");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx.options);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx.submitting);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.submitting);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", ctx.data == null ? null : ctx.data.command == null ? null : ctx.data.command.label, " ");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("diagram", ctx.diagram);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("visible", ctx.showLog);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"]("      ", ctx.log, "\n    ");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("visible", ctx.showError);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](10);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("visible", ctx.showCommandsModal);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](6);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx.selectedCommands);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_7__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_7__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_7__.NgIf, _angular_common__WEBPACK_IMPORTED_MODULE_7__.NgTemplateOutlet, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.CheckboxControlValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.NgModel, _modal_modal_component__WEBPACK_IMPORTED_MODULE_9__.ModalComponent, _diagram_diagram_component__WEBPACK_IMPORTED_MODULE_10__.DiagramComponent],
      styles: [".wizard-options[_ngcontent-%COMP%] {\n  height: calc(100vh - 4.5rem - 5.5rem - 3.5rem);\n}\n.wizard-options[_ngcontent-%COMP%]   .wizard-option[_ngcontent-%COMP%] {\n  position: relative;\n}\n.wizard-options[_ngcontent-%COMP%]   .wizard-option[_ngcontent-%COMP%]   .terminal[_ngcontent-%COMP%] {\n  position: absolute;\n  right: 0;\n  top: 50%;\n  margin-top: -8px;\n  width: 16px;\n  height: 16px;\n  display: none;\n  cursor: pointer;\n}\n.wizard-options[_ngcontent-%COMP%]   .wizard-option[_ngcontent-%COMP%]   .show[_ngcontent-%COMP%] {\n  display: block;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9hcmNoaXRlY3R1cmUtd2l6YXJkL2FyY2hpdGVjdHVyZS13aXphcmQuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBRUE7RUFDRSw4Q0FBQTtBQURGO0FBRUU7RUFDRSxrQkFBQTtBQUFKO0FBQ0k7RUFDRSxrQkFBQTtFQUNBLFFBQUE7RUFDQSxRQUFBO0VBQ0EsZ0JBQUE7RUFDQSxXQUFBO0VBQ0EsWUFBQTtFQUNBLGFBQUE7RUFDQSxlQUFBO0FBQ047QUFFSTtFQUNFLGNBQUE7QUFBTiIsInNvdXJjZXNDb250ZW50IjpbIkB1c2UgXCIuLi8uLi8uLi9nbG9iYWxzXCI7XG5cbi53aXphcmQtb3B0aW9ucyB7XG4gIGhlaWdodDogY2FsYygxMDB2aCAtICN7Z2xvYmFscy4kaGVhZGVyLWhlaWdodH0gLSAje2dsb2JhbHMuJGZvb3Rlci1oZWlnaHR9IC0gMy41cmVtKTtcbiAgLndpemFyZC1vcHRpb24ge1xuICAgIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgICAudGVybWluYWwge1xuICAgICAgcG9zaXRpb246IGFic29sdXRlO1xuICAgICAgcmlnaHQ6IDA7XG4gICAgICB0b3A6IDUwJTtcbiAgICAgIG1hcmdpbi10b3A6IC04cHg7XG4gICAgICB3aWR0aDogMTZweDtcbiAgICAgIGhlaWdodDogMTZweDtcbiAgICAgIGRpc3BsYXk6IG5vbmU7XG4gICAgICBjdXJzb3I6IHBvaW50ZXI7XG4gICAgfVxuXG4gICAgLnNob3cge1xuICAgICAgZGlzcGxheTogYmxvY2s7XG4gICAgfVxuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9 */"]
    });
  }
  return ArchitectureWizardComponent;
})();

/***/ }),

/***/ 7433:
/*!*******************************************************************!*\
  !*** ./src/app/components/architecture/architecture.component.ts ***!
  \*******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ArchitectureComponent: () => (/* binding */ ArchitectureComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_template_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../services/template.service */ 529);
/* harmony import */ var _services_info_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../services/info.service */ 957);
/* harmony import */ var _diagram_diagram_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../diagram/diagram.component */ 7254);




let ArchitectureComponent = /*#__PURE__*/(() => {
  class ArchitectureComponent {
    constructor(templateService, infoService) {
      this.templateService = templateService;
      this.infoService = infoService;
      this.diagram = {
        cellSize: 20,
        rows: 30,
        columns: 36,
        grid: false,
        icons: [],
        links: []
      };
    }
    ngOnInit() {
      this.templateService.getDiagramData('diagram', this.diagram).subscribe(result => {
        this.diagram = result;
        this.diagram.links = this.orderByDisabled(this.diagram.links);
      });
      const template = this.templateService.template$.getValue();
      const section = template.sections.find(s => s.id === 'architecture');
      if (section) {
        this.infoService.data = section.info || '';
      }
    }
    getIconById(id) {
      return this.diagram.icons.find(icon => icon.id === id);
    }
    isIconEnabled(id) {
      const icon = this.getIconById(id);
      return !!(icon && icon.display);
    }
    isLinkDisabled(link) {
      return !this.isIconEnabled(link.to) || !this.isIconEnabled(link.from);
    }
    orderByDisabled(links = []) {
      return links.sort((a, b) => Number(this.isLinkDisabled(b)) - Number(this.isLinkDisabled(a)));
    }
    static #_ = this.ɵfac = function ArchitectureComponent_Factory(t) {
      return new (t || ArchitectureComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_template_service__WEBPACK_IMPORTED_MODULE_1__.TemplateService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_info_service__WEBPACK_IMPORTED_MODULE_2__.InfoService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: ArchitectureComponent,
      selectors: [["theia-architecture"]],
      decls: 1,
      vars: 1,
      consts: [[3, "diagram"]],
      template: function ArchitectureComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "theia-diagram", 0);
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("diagram", ctx.diagram);
        }
      },
      dependencies: [_diagram_diagram_component__WEBPACK_IMPORTED_MODULE_3__.DiagramComponent],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return ArchitectureComponent;
})();

/***/ }),

/***/ 6410:
/*!***************************************************************!*\
  !*** ./src/app/components/auth-error/auth-error.component.ts ***!
  \***************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AuthErrorComponent: () => (/* binding */ AuthErrorComponent)
/* harmony export */ });
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../models/template */ 5339);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @auth0/auth0-angular */ 6742);
/* harmony import */ var _services_template_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../services/template.service */ 529);
/* harmony import */ var _error_error_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../error/error.component */ 9426);





let AuthErrorComponent = /*#__PURE__*/(() => {
  class AuthErrorComponent {
    constructor(authService, templateService) {
      this.authService = authService;
      this.templateService = templateService;
      this.error = {
        header: 'Unauthorized',
        error: '',
        description: ''
      };
    }
    ngOnInit() {
      this.templateService.template$.next({
        title: '',
        type: _models_template__WEBPACK_IMPORTED_MODULE_0__.TheiaType.Template,
        version: '',
        sections: [],
        footer: {
          "columns": []
        }
      });
      this.authService.error$.subscribe(error => {
        if (error.message === 'email_not_verified') {
          this.error = {
            header: 'Unauthorized',
            error: 'Email address not verified',
            description: 'Please check your email and verify your account'
          };
        }
      });
    }
    static #_ = this.ɵfac = function AuthErrorComponent_Factory(t) {
      return new (t || AuthErrorComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_2__.AuthService), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_template_service__WEBPACK_IMPORTED_MODULE_3__.TemplateService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineComponent"]({
      type: AuthErrorComponent,
      selectors: [["theia-auth-error"]],
      decls: 1,
      vars: 3,
      consts: [[3, "description", "error", "header"]],
      template: function AuthErrorComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](0, "theia-error", 0);
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("description", ctx.error.description)("error", ctx.error.error)("header", ctx.error.header);
        }
      },
      dependencies: [_error_error_component__WEBPACK_IMPORTED_MODULE_4__.ErrorComponent],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return AuthErrorComponent;
})();

/***/ }),

/***/ 2096:
/*!*************************************************************************!*\
  !*** ./src/app/components/composite-group/composite-group.component.ts ***!
  \*************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CompositeGroupComponent: () => (/* binding */ CompositeGroupComponent)
/* harmony export */ });
/* harmony import */ var _models_template_control__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../models/template/control */ 6347);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/forms */ 8849);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_dynamic_form_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../services/dynamic-form.service */ 449);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _dynamic_control_dynamic_control_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../dynamic-control/dynamic-control.component */ 1081);







function CompositeGroupComponent_ng_container_0_div_6_div_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 6)(1, "div", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](2, "theia-dynamic-control", 13);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const control_r5 = ctx.$implicit;
    const form_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    const ctx_r4 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("control", control_r5)("datasource", control_r5.datasource)("formControlName", control_r5.id)("parentForm", form_r2)("step", ctx_r4.step);
  }
}
function CompositeGroupComponent_ng_container_0_div_6_Template(rf, ctx) {
  if (rf & 1) {
    const _r8 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 8)(1, "div", 9)(2, "button", 10);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function CompositeGroupComponent_ng_container_0_div_6_Template_button_click_2_listener() {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r8);
      const i_r3 = restoredCtx.index;
      const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r7.delete(i_r3));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](3, "i", 11);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, CompositeGroupComponent_ng_container_0_div_6_div_4_Template, 3, 5, "div", 12);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const form_r2 = ctx.$implicit;
    const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formGroup", form_r2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r1.getGroupControls(form_r2));
  }
}
function CompositeGroupComponent_ng_container_0_Template(rf, ctx) {
  if (rf & 1) {
    const _r10 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0, 1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 2)(2, "div", 3)(3, "label");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](5, 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](6, CompositeGroupComponent_ng_container_0_div_6_Template, 5, 2, "div", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](7, "div", 6)(8, "div", 3)(9, "button", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function CompositeGroupComponent_ng_container_0_Template_button_click_9_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r10);
      const ctx_r9 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r9.add());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](10, "Add new");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formGroup", ctx_r0.parentForm);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", ctx_r0.group.label, " ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formArrayName", ctx_r0.group.id);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r0.arrayForm.controls);
  }
}
let CompositeGroupComponent = /*#__PURE__*/(() => {
  class CompositeGroupComponent {
    get arrayForm() {
      return this.parentForm.controls[this.group.id];
    }
    getGroupControls(form) {
      return form.groupControls || this.group.controls;
    }
    constructor(dynamicForm, cdr) {
      this.dynamicForm = dynamicForm;
      this.cdr = cdr;
      this.parentForm = new _angular_forms__WEBPACK_IMPORTED_MODULE_1__.UntypedFormGroup({});
      this.id = "";
      this.isCompositeGroupControl = _models_template_control__WEBPACK_IMPORTED_MODULE_2__.isCompositeGroupControl;
    }
    ngOnInit() {
      this.init();
    }
    ngOnChanges(changes) {
      if (changes.id.currentValue !== changes.id.previousValue) {
        this.init();
      }
    }
    init() {
      const formArray = this.parentForm.get(this.group.id);
      const form = new _angular_forms__WEBPACK_IMPORTED_MODULE_1__.UntypedFormGroup({});
      if (formArray?.length === 0) {
        const controls = this.group.controls.map(control => ({
          ...control
        }));
        this.dynamicForm.initialize(form, controls, this.cdr, {});
        form.groupControls = controls;
        formArray?.push(form);
      } else {
        formArray.controls.forEach(group => {
          const controls = this.group.controls.map(control => ({
            ...control
          }));
          this.dynamicForm.initialize(group, controls, this.cdr, {});
          group.groupControls = controls;
        });
      }
    }
    add() {
      const form = new _angular_forms__WEBPACK_IMPORTED_MODULE_1__.UntypedFormGroup({});
      const controls = this.group.controls.map(control => ({
        ...control
      }));
      form.groupControls = controls;
      this.dynamicForm.initialize(form, controls, this.cdr, {});
      this.parentForm.get(this.group.id)?.push(form);
    }
    delete(i) {
      this.parentForm.get(this.group.id)?.removeAt(i);
    }
    static #_ = this.ɵfac = function CompositeGroupComponent_Factory(t) {
      return new (t || CompositeGroupComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_dynamic_form_service__WEBPACK_IMPORTED_MODULE_3__.DynamicFormService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.ChangeDetectorRef));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: CompositeGroupComponent,
      selectors: [["theia-composite-group"]],
      inputs: {
        group: "group",
        parentForm: "parentForm",
        step: "step",
        id: "id"
      },
      features: [_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵNgOnChangesFeature"]],
      decls: 1,
      vars: 1,
      consts: [[3, "formGroup", 4, "ngIf"], [3, "formGroup"], [1, "row", "mb-3"], [1, "col"], [3, "formArrayName"], ["class", "card mb-3", 4, "ngFor", "ngForOf"], [1, "row"], [1, "btn", "btn-sm", "btn-outline-secondary", 3, "click"], [1, "card", "mb-3"], [1, "card-body", 3, "formGroup"], [1, "btn", "btn-sm", "btn-outline-danger", "delete", 3, "click"], [1, "bi", "bi-trash"], ["class", "row", 4, "ngFor", "ngForOf"], [1, "mb-3", 3, "control", "datasource", "formControlName", "parentForm", "step"]],
      template: function CompositeGroupComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](0, CompositeGroupComponent_ng_container_0_Template, 11, 4, "ng-container", 0);
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.group && ctx.isCompositeGroupControl(ctx.group));
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_4__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_4__.NgIf, _angular_forms__WEBPACK_IMPORTED_MODULE_1__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_1__.NgControlStatusGroup, _angular_forms__WEBPACK_IMPORTED_MODULE_1__.FormGroupDirective, _angular_forms__WEBPACK_IMPORTED_MODULE_1__.FormControlName, _angular_forms__WEBPACK_IMPORTED_MODULE_1__.FormArrayName, _dynamic_control_dynamic_control_component__WEBPACK_IMPORTED_MODULE_5__.DynamicControlComponent],
      styles: [".delete[_ngcontent-%COMP%] {\n  position: absolute;\n  right: 0.2rem;\n  top: 0.2rem;\n  padding: 0.3rem 0.6rem;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9jb21wb3NpdGUtZ3JvdXAvY29tcG9zaXRlLWdyb3VwLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0Usa0JBQUE7RUFDQSxhQUFBO0VBQ0EsV0FBQTtFQUNBLHNCQUFBO0FBQ0YiLCJzb3VyY2VzQ29udGVudCI6WyIuZGVsZXRlIHtcbiAgcG9zaXRpb246IGFic29sdXRlO1xuICByaWdodDogMC4ycmVtO1xuICB0b3A6IDAuMnJlbTtcbiAgcGFkZGluZzogMC4zcmVtIDAuNnJlbTtcbn1cbiJdLCJzb3VyY2VSb290IjoiIn0= */"]
    });
  }
  return CompositeGroupComponent;
})();

/***/ }),

/***/ 6530:
/*!*********************************************************************!*\
  !*** ./src/app/components/confirm-modal/confirm-modal.component.ts ***!
  \*********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ConfirmModalComponent: () => (/* binding */ ConfirmModalComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _modal_modal_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../modal/modal.component */ 354);



const _c0 = ["*"];
let ConfirmModalComponent = /*#__PURE__*/(() => {
  class ConfirmModalComponent {
    constructor() {
      this.title = '';
      this.visible = false;
      this.dismiss = new _angular_core__WEBPACK_IMPORTED_MODULE_0__.EventEmitter();
    }
    handleClose(confirm) {
      this.visible = false;
      this.dismiss.emit(confirm);
    }
    static #_ = this.ɵfac = function ConfirmModalComponent_Factory(t) {
      return new (t || ConfirmModalComponent)();
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: ConfirmModalComponent,
      selectors: [["theia-confirm-modal"]],
      inputs: {
        title: "title",
        visible: "visible"
      },
      outputs: {
        dismiss: "dismiss"
      },
      ngContentSelectors: _c0,
      decls: 12,
      vars: 2,
      consts: [["classes", "modal-dialog-centered", 3, "visible"], ["slot", "header"], [1, "modal-title"], ["type", "button", "data-bs-dismiss", "modal", "aria-label", "Close", 1, "btn-close", 3, "click"], ["slot", "body"], ["slot", "footer"], ["type", "button", 1, "btn", "btn-outline-secondary", "flex-fill", 3, "click"], ["type", "button", 1, "btn", "btn-primary", "flex-fill", 3, "click"]],
      template: function ConfirmModalComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵprojectionDef"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "theia-modal", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](1, 1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "h5", 2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "button", 3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function ConfirmModalComponent_Template_button_click_4_listener() {
            return ctx.handleClose(false);
          });
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](5, 4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵprojection"](6);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](7, 5);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](8, "button", 6);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function ConfirmModalComponent_Template_button_click_8_listener() {
            return ctx.handleClose(false);
          });
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](9, "Cancel");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](10, "button", 7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function ConfirmModalComponent_Template_button_click_10_listener() {
            return ctx.handleClose(true);
          });
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](11, "Confirm");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("visible", ctx.visible);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](ctx.title);
        }
      },
      dependencies: [_modal_modal_component__WEBPACK_IMPORTED_MODULE_1__.ModalComponent],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return ConfirmModalComponent;
})();

/***/ }),

/***/ 5863:
/*!**********************************************************************************!*\
  !*** ./src/app/components/dashboard/components/dashboard/dashboard.component.ts ***!
  \**********************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DashboardComponent: () => (/* binding */ DashboardComponent)
/* harmony export */ });
/* harmony import */ var _models_template_dashboard__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../models/template/dashboard */ 1657);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _directives_typed_template_directive__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../directives/typed-template.directive */ 7105);
/* harmony import */ var _panel_markdown_panel_markdown_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../panel-markdown/panel-markdown.component */ 169);
/* harmony import */ var _panel_table_panel_table_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../panel-table/panel-table.component */ 522);






const _c0 = function (a0) {
  return {
    row: a0
  };
};
function DashboardComponent_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainer"](0, 4);
  }
  if (rf & 2) {
    const row_r3 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    const _r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngTemplateOutlet", _r1)("ngTemplateOutletContext", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](2, _c0, row_r3));
  }
}
function DashboardComponent_ng_template_2_ng_container_1_div_2_theia_panel_markdown_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "theia-panel-markdown", 15);
  }
  if (rf & 2) {
    const col_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2).$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("content", col_r6.panel.content);
  }
}
function DashboardComponent_ng_template_2_ng_container_1_div_2_theia_panel_table_5_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "theia-panel-table", 16);
  }
  if (rf & 2) {
    const col_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2).$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("panel", col_r6.panel);
  }
}
function DashboardComponent_ng_template_2_ng_container_1_div_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 10)(1, "h6", 11);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "div", 12);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, DashboardComponent_ng_template_2_ng_container_1_div_2_theia_panel_markdown_4_Template, 1, 1, "theia-panel-markdown", 13);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](5, DashboardComponent_ng_template_2_ng_container_1_div_2_theia_panel_table_5_Template, 1, 1, "theia-panel-table", 14);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const col_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", col_r6.panel.title, " ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", col_r6.panel.type === ctx_r7.PanelType.Markdown);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", col_r6.panel.type === ctx_r7.PanelType.Table);
  }
}
function DashboardComponent_ng_template_2_ng_container_1_ng_container_3_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainer"](0, 4);
  }
  if (rf & 2) {
    const child_r15 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
    const _r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngTemplateOutlet", _r1)("ngTemplateOutletContext", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](2, _c0, child_r15));
  }
}
function DashboardComponent_ng_template_2_ng_container_1_ng_container_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, DashboardComponent_ng_template_2_ng_container_1_ng_container_3_ng_container_1_Template, 1, 4, "ng-container", 1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const col_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", col_r6.rows);
  }
}
function DashboardComponent_ng_template_2_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, DashboardComponent_ng_template_2_ng_container_1_div_2_Template, 6, 3, "div", 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, DashboardComponent_ng_template_2_ng_container_1_ng_container_3_Template, 2, 1, "ng-container", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const col_r6 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", col_r6.size ? "col-" + col_r6.size : "col");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", col_r6.panel && !col_r6.rows);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", col_r6.rows && !col_r6.panel);
  }
}
function DashboardComponent_ng_template_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, DashboardComponent_ng_template_2_ng_container_1_Template, 4, 3, "ng-container", 6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const row_r4 = ctx.row;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", row_r4.columns);
  }
}
let DashboardComponent = /*#__PURE__*/(() => {
  class DashboardComponent {
    constructor() {
      this.rows = [];
      this.PanelType = _models_template_dashboard__WEBPACK_IMPORTED_MODULE_1__.PanelType;
    }
    static #_ = this.ɵfac = function DashboardComponent_Factory(t) {
      return new (t || DashboardComponent)();
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: DashboardComponent,
      selectors: [["theia-dashboard"]],
      inputs: {
        rows: "rows"
      },
      decls: 4,
      vars: 2,
      consts: [[1, "container"], [3, "ngTemplateOutlet", "ngTemplateOutletContext", 4, "ngFor", "ngForOf"], [3, "typedTemplate"], ["rowsTemplate", ""], [3, "ngTemplateOutlet", "ngTemplateOutletContext"], [1, "row", "mb-3"], [4, "ngFor", "ngForOf"], [3, "ngClass"], ["class", "card", 4, "ngIf"], [4, "ngIf"], [1, "card"], [1, "card-header"], [1, "card-body"], [3, "content", 4, "ngIf"], [3, "panel", 4, "ngIf"], [3, "content"], [3, "panel"]],
      template: function DashboardComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, DashboardComponent_ng_container_1_Template, 1, 4, "ng-container", 1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, DashboardComponent_ng_template_2_Template, 2, 1, "ng-template", 2, 3, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplateRefExtractor"]);
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx.rows);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("typedTemplate", ctx.typeToken);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_2__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_2__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_2__.NgIf, _angular_common__WEBPACK_IMPORTED_MODULE_2__.NgTemplateOutlet, _directives_typed_template_directive__WEBPACK_IMPORTED_MODULE_3__.TypedTemplateDirective, _panel_markdown_panel_markdown_component__WEBPACK_IMPORTED_MODULE_4__.PanelMarkdownComponent, _panel_table_panel_table_component__WEBPACK_IMPORTED_MODULE_5__.PanelTableComponent],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return DashboardComponent;
})();

/***/ }),

/***/ 169:
/*!********************************************************************************************!*\
  !*** ./src/app/components/dashboard/components/panel-markdown/panel-markdown.component.ts ***!
  \********************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PanelMarkdownComponent: () => (/* binding */ PanelMarkdownComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var ngx_markdown__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ngx-markdown */ 1995);


let PanelMarkdownComponent = /*#__PURE__*/(() => {
  class PanelMarkdownComponent {
    constructor() {
      this.content = '';
    }
    static #_ = this.ɵfac = function PanelMarkdownComponent_Factory(t) {
      return new (t || PanelMarkdownComponent)();
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: PanelMarkdownComponent,
      selectors: [["theia-panel-markdown"]],
      inputs: {
        content: "content"
      },
      decls: 1,
      vars: 1,
      consts: [[3, "data"]],
      template: function PanelMarkdownComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "markdown", 0);
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("data", ctx.content);
        }
      },
      dependencies: [ngx_markdown__WEBPACK_IMPORTED_MODULE_1__.MarkdownComponent],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return PanelMarkdownComponent;
})();

/***/ }),

/***/ 522:
/*!**************************************************************************************!*\
  !*** ./src/app/components/dashboard/components/panel-table/panel-table.component.ts ***!
  \**************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PanelTableComponent: () => (/* binding */ PanelTableComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_data_source_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../services/data-source.service */ 6678);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ 6575);



function PanelTableComponent_div_0_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 2)(1, "div", 3)(2, "span", 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](3, "Loading...");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
  }
}
function PanelTableComponent_ng_template_1_p_0_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "p");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](ctx_r3.panel.description);
  }
}
function PanelTableComponent_ng_template_1_th_5_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const column_r8 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", column_r8.label, " ");
  }
}
function PanelTableComponent_ng_template_1_ng_container_7_tr_1_td_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const value_r12 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", value_r12, " ");
  }
}
function PanelTableComponent_ng_template_1_ng_container_7_tr_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "tr");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, PanelTableComponent_ng_template_1_ng_container_7_tr_1_td_1_Template, 2, 1, "td", 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const row_r10 = ctx.$implicit;
    const ctx_r9 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r9.getValues(row_r10));
  }
}
function PanelTableComponent_ng_template_1_ng_container_7_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, PanelTableComponent_ng_template_1_ng_container_7_tr_1_Template, 2, 1, "tr", 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r5 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r5.data);
  }
}
function PanelTableComponent_ng_template_1_ng_template_8_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "tr", 11)(1, "td", 12);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2, " No results found ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("colSpan", ctx_r7.panel.columns == null ? null : ctx_r7.panel.columns.length);
  }
}
function PanelTableComponent_ng_template_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](0, PanelTableComponent_ng_template_1_p_0_Template, 2, 1, "p", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 6)(2, "table", 7)(3, "thead")(4, "tr");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](5, PanelTableComponent_ng_template_1_th_5_Template, 2, 1, "th", 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](6, "tbody");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](7, PanelTableComponent_ng_template_1_ng_container_7_Template, 2, 1, "ng-container", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](8, PanelTableComponent_ng_template_1_ng_template_8_Template, 3, 1, "ng-template", null, 10, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplateRefExtractor"]);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
  }
  if (rf & 2) {
    const _r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](9);
    const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r2.panel.description);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r2.panel.columns);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r2.data.length)("ngIfElse", _r6);
  }
}
let PanelTableComponent = /*#__PURE__*/(() => {
  class PanelTableComponent {
    constructor(dataSourceService) {
      this.dataSourceService = dataSourceService;
      this.data = [];
      this.loading = true;
    }
    ngOnInit() {
      this.dataSourceService.getData(this.panel.datasource, this.panel.env_required).subscribe(data => {
        this.loading = false;
        this.data = data;
      });
    }
    getValues(row) {
      return this.panel.columns.map(column => row[column.key]);
    }
    static #_ = this.ɵfac = function PanelTableComponent_Factory(t) {
      return new (t || PanelTableComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_data_source_service__WEBPACK_IMPORTED_MODULE_1__.DataSourceService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: PanelTableComponent,
      selectors: [["theia-panel-table"]],
      inputs: {
        panel: "panel"
      },
      decls: 3,
      vars: 2,
      consts: [["class", "d-flex justify-content-center loader", 4, "ngIf", "ngIfElse"], ["loaded", ""], [1, "d-flex", "justify-content-center", "loader"], ["role", "status", 1, "spinner-border", "spinner-big", "m-4", "text-primary"], [1, "visually-hidden"], [4, "ngIf"], [1, "table-responsive"], [1, "table", "table-striped", "table-hover", "table-sm", "table-bordered", "text-nowrap"], [4, "ngFor", "ngForOf"], [4, "ngIf", "ngIfElse"], ["noResults", ""], [1, "text-center"], [3, "colSpan"]],
      template: function PanelTableComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](0, PanelTableComponent_div_0_Template, 4, 0, "div", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, PanelTableComponent_ng_template_1_Template, 10, 4, "ng-template", null, 1, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplateRefExtractor"]);
        }
        if (rf & 2) {
          const _r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.loading)("ngIfElse", _r1);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_2__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_2__.NgIf],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return PanelTableComponent;
})();

/***/ }),

/***/ 1010:
/*!**********************************************************!*\
  !*** ./src/app/components/dashboard/dashboard.module.ts ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DashboardModule: () => (/* binding */ DashboardModule)
/* harmony export */ });
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _components_dashboard_dashboard_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/dashboard/dashboard.component */ 5863);
/* harmony import */ var _directives_typed_template_directive__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./directives/typed-template.directive */ 7105);
/* harmony import */ var _components_panel_markdown_panel_markdown_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/panel-markdown/panel-markdown.component */ 169);
/* harmony import */ var ngx_markdown__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ngx-markdown */ 1995);
/* harmony import */ var _components_panel_table_panel_table_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components/panel-table/panel-table.component */ 522);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);







let DashboardModule = /*#__PURE__*/(() => {
  class DashboardModule {
    static #_ = this.ɵfac = function DashboardModule_Factory(t) {
      return new (t || DashboardModule)();
    };
    static #_2 = this.ɵmod = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineNgModule"]({
      type: DashboardModule
    });
    static #_3 = this.ɵinj = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjector"]({
      imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__.CommonModule, ngx_markdown__WEBPACK_IMPORTED_MODULE_2__.MarkdownModule]
    });
  }
  return DashboardModule;
})();
(function () {
  (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsetNgModuleScope"](DashboardModule, {
    declarations: [_components_dashboard_dashboard_component__WEBPACK_IMPORTED_MODULE_3__.DashboardComponent, _directives_typed_template_directive__WEBPACK_IMPORTED_MODULE_4__.TypedTemplateDirective, _components_panel_markdown_panel_markdown_component__WEBPACK_IMPORTED_MODULE_5__.PanelMarkdownComponent, _components_panel_table_panel_table_component__WEBPACK_IMPORTED_MODULE_6__.PanelTableComponent],
    imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__.CommonModule, ngx_markdown__WEBPACK_IMPORTED_MODULE_2__.MarkdownModule],
    exports: [_components_dashboard_dashboard_component__WEBPACK_IMPORTED_MODULE_3__.DashboardComponent, _components_panel_markdown_panel_markdown_component__WEBPACK_IMPORTED_MODULE_5__.PanelMarkdownComponent]
  });
})();

/***/ }),

/***/ 7105:
/*!*****************************************************************************!*\
  !*** ./src/app/components/dashboard/directives/typed-template.directive.ts ***!
  \*****************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TypedTemplateDirective: () => (/* binding */ TypedTemplateDirective)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);

let TypedTemplateDirective = /*#__PURE__*/(() => {
  class TypedTemplateDirective {
    constructor(contentTemplate) {
      this.contentTemplate = contentTemplate;
    }
    // this magic is how we tell Angular the context type for this directive, which then propagates down to the type of the template
    static ngTemplateContextGuard(dir, ctx) {
      return true;
    }
    static #_ = this.ɵfac = function TypedTemplateDirective_Factory(t) {
      return new (t || TypedTemplateDirective)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.TemplateRef));
    };
    static #_2 = this.ɵdir = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineDirective"]({
      type: TypedTemplateDirective,
      selectors: [["ng-template", "typedTemplate", ""]],
      inputs: {
        typeToken: ["typedTemplate", "typeToken"]
      }
    });
  }
  return TypedTemplateDirective;
})();

/***/ }),

/***/ 7254:
/*!*********************************************************!*\
  !*** ./src/app/components/diagram/diagram.component.ts ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DiagramComponent: () => (/* binding */ DiagramComponent)
/* harmony export */ });
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);



function DiagramComponent__svg_g_14__svg_circle_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "circle", 15);
  }
  if (rf & 2) {
    const icon_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    const ctx_r4 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵattribute"]("cx", ctx_r4.toPixels(icon_r3.x) + ctx_r4.diagram.cellSize)("cy", ctx_r4.toPixels(icon_r3.y))("fill", icon_r3.active ? "green" : "red")("r", ctx_r4.relativeSize(8));
  }
}
function DiagramComponent__svg_g_14_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "g")(1, "text");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](3, "image");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, DiagramComponent__svg_g_14__svg_circle_4_Template, 1, 4, "circle", 14);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const icon_r3 = ctx.$implicit;
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵattribute"]("font-size", ctx_r0.relativeSize(16))("stroke-width", !icon_r3.display ? ".5" : "")("stroke", !icon_r3.display ? "#ccc" : "")("transform", ctx_r0.translateCenter(icon_r3.text))("x", ctx_r0.toPixels(icon_r3.x))("y", ctx_r0.toPixels(icon_r3.y) + ctx_r0.diagram.cellSize + ctx_r0.relativeSize(20));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", icon_r3.text, " ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵstyleProp"]("filter", icon_r3.display ? "none" : "url(#grayscale)");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵattribute"]("height", ctx_r0.diagram.cellSize)("opacity", icon_r3.display ? 1 : 0.3)("width", ctx_r0.diagram.cellSize)("x", ctx_r0.toPixels(icon_r3.x))("href", icon_r3.url, null, "xlink")("y", ctx_r0.toPixels(icon_r3.y));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", icon_r3.active !== undefined && icon_r3.active !== null && icon_r3.display);
  }
}
function DiagramComponent__svg_ng_container_15__svg_g_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "g", 17);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "path");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const link_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵattribute"]("stroke-width", 0.8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵattribute"]("d", ctx_r7.getPath(link_r6.path))("marker-end", ctx_r7.getMarkerEnd(link_r6))("marker-start", ctx_r7.getMarkerStart(link_r6))("stroke-dasharray", ctx_r7.isLinkDisabled(link_r6) ? "4 6" : "")("stroke", ctx_r7.isLinkDisabled(link_r6) ? "#ccc" : "#999");
  }
}
function DiagramComponent__svg_ng_container_15_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, DiagramComponent__svg_ng_container_15__svg_g_1_Template, 2, 6, "g", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const link_r6 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", link_r6.from && link_r6.to);
  }
}
function DiagramComponent__svg_ng_container_16__svg_ng_container_2__svg_text_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "text", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const cell_r13 = ctx.$implicit;
    const x_r14 = ctx.index;
    const y_r11 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().index;
    const ctx_r12 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵattribute"]("font-size", ctx_r12.relativeSize(12))("x", cell_r13.x)("y", cell_r13.y);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate2"](" ", x_r14, ",", y_r11, " ");
  }
}
function DiagramComponent__svg_ng_container_16__svg_ng_container_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, DiagramComponent__svg_ng_container_16__svg_ng_container_2__svg_text_1_Template, 2, 5, "text", 19);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const row_r10 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", row_r10);
  }
}
function DiagramComponent__svg_ng_container_16_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "rect", 18);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, DiagramComponent__svg_ng_container_16__svg_ng_container_2_Template, 2, 1, "ng-container", 12);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r2.cells);
  }
}
let DiagramComponent = /*#__PURE__*/(() => {
  class DiagramComponent {
    constructor(document) {
      this.document = document;
      this.diagram = {
        cellSize: 0,
        rows: 0,
        columns: 0,
        grid: false,
        icons: [],
        links: []
      };
      this.defaultSize = 50;
    }
    get svgWidth() {
      return this.diagram.columns * this.diagram.cellSize;
    }
    get svgHeight() {
      return this.diagram.rows * this.diagram.cellSize;
    }
    get cells() {
      return [...Array(this.diagram.rows).keys()].map(y => {
        return [...Array(this.diagram.columns).keys()].map(x => ({
          x: this.toPixels(x),
          y: this.toPixels(y) + this.relativeSize(10)
        }));
      });
    }
    toPixels(size) {
      return size * this.diagram.cellSize;
    }
    relativeSize(size) {
      return this.toPixels(size) / this.defaultSize;
    }
    calculateTextWidth(text) {
      const svg = this.document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      const textNode = this.document.createElementNS('http://www.w3.org/2000/svg', 'text');
      textNode.setAttributeNS(null, 'stroke', 'transparent');
      textNode.setAttributeNS(null, 'font-size', this.relativeSize(16).toString());
      textNode.textContent = text;
      svg.appendChild(textNode);
      const body = this.document.querySelector('body') || this.document.createElement('body');
      body.appendChild(svg);
      const rect = textNode.getBoundingClientRect();
      body.removeChild(svg);
      return rect.width;
    }
    translateCenter(text) {
      const width = this.calculateTextWidth(text);
      return `translate(${(this.diagram.cellSize - width) / 2})`;
    }
    getMarkerStart(link) {
      return link.markerStart ? `url(#arrowStart${this.isLinkDisabled(link) ? 'Light' : ''})` : 'none';
    }
    getMarkerEnd(link) {
      return link.markerEnd ? `url(#arrowEnd${this.isLinkDisabled(link) ? 'Light' : ''})` : 'none';
    }
    getPath(path) {
      return path.reduce((result, curr, index, arr) => {
        let command = 'L';
        let dx;
        let dy;
        const xPixels = this.toPixels(Number(curr.x));
        const yPixels = this.toPixels(Number(curr.y));
        const halfCell = this.diagram.cellSize / 2;
        const quarterCell = halfCell / 2;
        const offsetX = curr.offsetX || 0;
        const offsetY = curr.offsetY || 0;
        dx = xPixels + halfCell + quarterCell * offsetX;
        dy = yPixels + halfCell + quarterCell * offsetY;
        if (index === 0) {
          command = 'M';
          const next = arr[index + 1];
          if (next) {
            if (Number(next.x) > Number(curr.x)) {
              dx = xPixels + this.diagram.cellSize;
            } else if (Number(next.x) < Number(curr.x)) {
              dx = xPixels;
            }
            if (Number(next.y) > Number(curr.y)) {
              dy = yPixels + this.diagram.cellSize;
            } else if (Number(next.y) < Number(curr.y)) {
              dy = yPixels;
            }
          }
        }
        if (index === arr.length - 1) {
          const prev = arr[index - 1];
          if (prev) {
            if (Number(curr.x) > Number(prev.x)) {
              dx = xPixels;
            } else if (Number(curr.x) < Number(prev.x)) {
              dx = xPixels + this.diagram.cellSize;
            }
            if (Number(curr.y) > Number(prev.y)) {
              dy = yPixels;
            } else if (Number(curr.y) < Number(prev.y)) {
              dy = yPixels + this.diagram.cellSize;
            }
          }
        }
        return `${result} ${command}${dx},${dy}`;
      }, '');
    }
    getIconById(id) {
      return this.diagram.icons.find(icon => Number(icon.id) === Number(id));
    }
    isIconEnabled(id) {
      const icon = this.getIconById(id);
      return !!(icon && icon.display);
    }
    isLinkDisabled(link) {
      return !this.isIconEnabled(link.to) || !this.isIconEnabled(link.from);
    }
    static #_ = this.ɵfac = function DiagramComponent_Factory(t) {
      return new (t || DiagramComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_common__WEBPACK_IMPORTED_MODULE_1__.DOCUMENT));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: DiagramComponent,
      selectors: [["theia-diagram"]],
      inputs: {
        diagram: "diagram"
      },
      decls: 17,
      vars: 8,
      consts: [["id", "arrowEnd", "markerHeight", "8", "markerWidth", "8", "orient", "auto", "refX", "9", "viewBox", "0 -5 10 10"], ["d", "M0,-5L10,0L0,5", "fill", "#999"], ["id", "arrowStart", "markerHeight", "8", "markerWidth", "8", "orient", "auto", "refX", "0", "viewBox", "0 -5 10 10"], ["d", "M0,0,L10,5,L10,-5", "fill", "#999"], ["id", "arrowEndLight", "markerHeight", "8", "markerWidth", "8", "orient", "auto", "refX", "9", "viewBox", "0 -5 10 10"], ["d", "M0,-5L10,0L0,5", "fill", "#ccc"], ["id", "arrowStartLight", "markerHeight", "8", "markerWidth", "8", "orient", "auto", "refX", "0", "viewBox", "0 -5 10 10"], ["d", "M0,0,L10,5,L10,-5", "fill", "#ccc"], ["id", "grid", "patternUnits", "userSpaceOnUse"], ["fill", "none", "stroke", "gray", "stroke-width", "1"], ["id", "grayscale"], ["type", "saturate", "values", "0.05"], [4, "ngFor", "ngForOf"], [4, "ngIf"], ["stroke", "black", "stroke-width", "1", 4, "ngIf"], ["stroke", "black", "stroke-width", "1"], ["fill", "none", 4, "ngIf"], ["fill", "none"], ["fill", "url(#grid)", "height", "100%", "width", "100%"], ["fill", "gray", 4, "ngFor", "ngForOf"], ["fill", "gray"]],
      template: function DiagramComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "svg")(1, "defs")(2, "marker", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](3, "path", 1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "marker", 2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](5, "path", 3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](6, "marker", 4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](7, "path", 5);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](8, "marker", 6);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](9, "path", 7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](10, "pattern", 8);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](11, "path", 9);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](12, "filter", 10);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](13, "feColorMatrix", 11);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](14, DiagramComponent__svg_g_14_Template, 5, 16, "g", 12);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](15, DiagramComponent__svg_ng_container_15_Template, 2, 1, "ng-container", 12);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](16, DiagramComponent__svg_ng_container_16_Template, 3, 1, "ng-container", 13);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵattribute"]("height", ctx.svgHeight)("width", ctx.svgWidth);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](10);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵattribute"]("height", ctx.diagram.cellSize)("width", ctx.diagram.cellSize);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵattribute"]("d", "M " + ctx.diagram.cellSize + " 0 L 0 0 0 " + ctx.diagram.cellSize);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx.diagram.icons);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx.diagram.links);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.diagram.grid);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_1__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_1__.NgIf],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return DiagramComponent;
})();

/***/ }),

/***/ 334:
/*!***********************************************************************!*\
  !*** ./src/app/components/dynamic-action/dynamic-action.component.ts ***!
  \***********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DynamicActionComponent: () => (/* binding */ DynamicActionComponent)
/* harmony export */ });
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../models/template */ 5339);
/* harmony import */ var _directives_static_action_directive__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../directives/static-action.directive */ 7637);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_template_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../services/template.service */ 529);
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ 7947);
/* harmony import */ var _services_environment_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/environment.service */ 1574);
/* harmony import */ var _services_info_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/info.service */ 957);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var ngx_markdown__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ngx-markdown */ 1995);
/* harmony import */ var _dashboard_components_dashboard_dashboard_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../dashboard/components/dashboard/dashboard.component */ 5863);
/* harmony import */ var _steps_steps_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../steps/steps.component */ 5770);
/* harmony import */ var _layout_layout_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../layout/layout.component */ 2952);













const _c0 = function () {
  return [];
};
function DynamicActionComponent_ng_container_1_ng_container_1_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "theia-steps", 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r5 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("actionId", ctx_r5.currentAction.id)("steps", ctx_r5.currentAction.steps || _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction0"](4, _c0))("sectionLabel", ctx_r5.section == null ? null : ctx_r5.section.label)("actionLabel", ctx_r5.currentAction.label);
  }
}
function DynamicActionComponent_ng_container_1_ng_container_1_ng_container_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "theia-dashboard", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("rows", ctx_r6.currentAction.rows || _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction0"](1, _c0));
  }
}
function DynamicActionComponent_ng_container_1_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, DynamicActionComponent_ng_container_1_ng_container_1_ng_container_1_Template, 2, 5, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, DynamicActionComponent_ng_container_1_ng_container_1_ng_container_2_Template, 2, 2, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r2.currentAction && ctx_r2.currentAction.type === ctx_r2.TheiaType.Action);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r2.currentAction && ctx_r2.currentAction.type === ctx_r2.TheiaType.Dashboard);
  }
}
function DynamicActionComponent_ng_container_1_ng_template_2_markdown_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "markdown", 10);
  }
  if (rf & 2) {
    const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("data", ctx_r7.section == null ? null : ctx_r7.section.description);
  }
}
function DynamicActionComponent_ng_container_1_ng_template_2_p_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "p", 11);
  }
  if (rf & 2) {
    const ctx_r8 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("innerHTML", ctx_r8.section == null ? null : ctx_r8.section.description, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsanitizeHtml"]);
  }
}
function DynamicActionComponent_ng_container_1_ng_template_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 6)(1, "div", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, DynamicActionComponent_ng_container_1_ng_template_2_markdown_2_Template, 1, 1, "markdown", 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, DynamicActionComponent_ng_container_1_ng_template_2_p_3_Template, 1, 1, "p", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r4 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r4.section == null ? null : ctx_r4.section.allowMarkdown);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !(ctx_r4.section == null ? null : ctx_r4.section.allowMarkdown));
  }
}
function DynamicActionComponent_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, DynamicActionComponent_ng_container_1_ng_container_1_Template, 3, 2, "ng-container", 2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, DynamicActionComponent_ng_container_1_ng_template_2_Template, 4, 2, "ng-template", null, 3, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplateRefExtractor"]);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const _r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](3);
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r0.currentAction)("ngIfElse", _r3);
  }
}
function DynamicActionComponent_ng_template_3_Template(rf, ctx) {}
let DynamicActionComponent = /*#__PURE__*/(() => {
  class DynamicActionComponent {
    constructor(templateService, activatedRoute, environmentService, cdr, info, componentFactoryResolver) {
      this.templateService = templateService;
      this.activatedRoute = activatedRoute;
      this.environmentService = environmentService;
      this.cdr = cdr;
      this.info = info;
      this.componentFactoryResolver = componentFactoryResolver;
      this.currentStepIndex = 0;
      this.TheiaType = _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaType;
      this.currentEnv$ = environmentService.getCurrentEnvironment();
    }
    ngOnInit() {
      this.activatedRoute.paramMap.subscribe(params => {
        const route = params.get('route') || '';
        const action = params.get('action') || '';
        this.section = this.templateService.getSectionByRoute(route);
        this.currentAction = this.templateService.getActionById(route, action);
        if (this.currentAction && this.currentAction.dynamic && this.currentAction.component && (this.currentEnv$.value || this.currentAction.env_not_required)) {
          this.loadDynamicComponent(this.currentAction.component);
        } else {
          this.staticHost?.viewContainerRef?.clear();
        }
        this.info.data = this.currentAction?.info || "";
      });
      this.environmentService.getCurrentEnvironment().subscribe(() => {
        const action = this.currentAction;
        this.currentAction = undefined;
        this.cdr.detectChanges();
        this.currentAction = action;
      });
    }
    loadDynamicComponent(component) {
      const file = component.file;
      const className = component.className;
      __webpack_require__(3653)(`./${file}/${file}.component.ts`).then(module => {
        setTimeout(() => {
          const componentFactory = this.componentFactoryResolver.resolveComponentFactory(module[className]);
          const viewContainerRef = this.staticHost.viewContainerRef;
          viewContainerRef.clear();
          const componentRef = viewContainerRef.createComponent(componentFactory);
          componentRef.instance.data = component.data;
        }, 0);
      });
    }
    static #_ = this.ɵfac = function DynamicActionComponent_Factory(t) {
      return new (t || DynamicActionComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_template_service__WEBPACK_IMPORTED_MODULE_2__.TemplateService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_router__WEBPACK_IMPORTED_MODULE_3__.ActivatedRoute), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_environment_service__WEBPACK_IMPORTED_MODULE_4__.EnvironmentService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.ChangeDetectorRef), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_info_service__WEBPACK_IMPORTED_MODULE_5__.InfoService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.ComponentFactoryResolver));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: DynamicActionComponent,
      selectors: [["theia-dynamic-action"]],
      viewQuery: function DynamicActionComponent_Query(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵviewQuery"](_directives_static_action_directive__WEBPACK_IMPORTED_MODULE_6__.StaticActionDirective, 7);
        }
        if (rf & 2) {
          let _t;
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.staticHost = _t.first);
        }
      },
      decls: 4,
      vars: 3,
      consts: [[4, "ngIf"], ["theiaStaticAction", ""], [4, "ngIf", "ngIfElse"], ["showDescription", ""], [3, "actionId", "steps", "sectionLabel", "actionLabel"], [1, "row", 3, "rows"], [1, "card"], [1, "card-body"], [3, "data", 4, "ngIf"], [3, "innerHTML", 4, "ngIf"], [3, "data"], [3, "innerHTML"]],
      template: function DynamicActionComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "theia-layout");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, DynamicActionComponent_ng_container_1_Template, 4, 2, "ng-container", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](2, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, DynamicActionComponent_ng_template_3_Template, 0, 0, "ng-template", 1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](2, 1, ctx.currentEnv$) || (ctx.currentAction == null ? null : ctx.currentAction.env_not_required));
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_7__.NgIf, ngx_markdown__WEBPACK_IMPORTED_MODULE_8__.MarkdownComponent, _dashboard_components_dashboard_dashboard_component__WEBPACK_IMPORTED_MODULE_9__.DashboardComponent, _steps_steps_component__WEBPACK_IMPORTED_MODULE_10__.StepsComponent, _layout_layout_component__WEBPACK_IMPORTED_MODULE_11__.LayoutComponent, _directives_static_action_directive__WEBPACK_IMPORTED_MODULE_6__.StaticActionDirective, _angular_common__WEBPACK_IMPORTED_MODULE_7__.AsyncPipe],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return DynamicActionComponent;
})();

/***/ }),

/***/ 1081:
/*!*************************************************************************!*\
  !*** ./src/app/components/dynamic-control/dynamic-control.component.ts ***!
  \*************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DynamicControlComponent: () => (/* binding */ DynamicControlComponent)
/* harmony export */ });
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ 8849);
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../models/template */ 7044);
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../models/template */ 1249);
/* harmony import */ var ng2_file_upload__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ng2-file-upload */ 8079);
/* harmony import */ var mime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! mime */ 6695);
/* harmony import */ var mime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(mime__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _models_template_control__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../models/template/control */ 6347);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_data_source_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../services/data-source.service */ 6678);
/* harmony import */ var _services_command_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../services/command.service */ 9167);
/* harmony import */ var _services_s3_upload_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../services/s3-upload.service */ 8427);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @ng-select/ng-select */ 1788);
/* harmony import */ var _directives_control_attributes_directive__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../directives/control-attributes.directive */ 2432);
/* harmony import */ var _key_value_editor_key_value_editor_component__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../key-value-editor/key-value-editor.component */ 1052);
/* harmony import */ var ngx_markdown__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ngx-markdown */ 1995);
/* harmony import */ var _pipes_file_size_pipe__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ../../pipes/file-size.pipe */ 77);

















const _c0 = function (a0) {
  return {
    "is-invalid": a0
  };
};
function DynamicControlComponent_ng_container_0_div_2_input_3_Template(rf, ctx) {
  if (rf & 1) {
    const _r14 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "input", 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("blur", function DynamicControlComponent_ng_container_0_div_2_input_3_Template_input_blur_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r14);
      const ctx_r13 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r13.handleBlur());
    })("input", function DynamicControlComponent_ng_container_0_div_2_input_3_Template_input_input_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r14);
      const ctx_r15 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r15.handleInput($event));
    })("ngModelChange", function DynamicControlComponent_ng_container_0_div_2_input_3_Template_input_ngModelChange_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r14);
      const ctx_r16 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r16.value = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r11 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", ctx_r11.value)("disabled", ctx_r11.disabled)("id", ctx_r11.control.id)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpureFunction1"](8, _c0, ctx_r11.invalid))("theiaControlAttributes", ctx_r11.control.attributes)("type", ctx_r11.control.inputType || "text")("readonly", ctx_r11.readonly);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵattribute"]("aria-described-by", ctx_r11.control.id + "Help");
  }
}
function DynamicControlComponent_ng_container_0_div_2_ng_template_4_Template(rf, ctx) {}
function DynamicControlComponent_ng_container_0_div_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 4)(1, "label", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](3, DynamicControlComponent_ng_container_0_div_2_input_3_Template, 1, 10, "input", 6);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](4, DynamicControlComponent_ng_container_0_div_2_ng_template_4_Template, 0, 0, "ng-template", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2);
    const _r1 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵreference"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngClass", ctx_r3.class);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("htmlFor", ctx_r3.control.id);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r3.control.label);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r3.isInputControl(ctx_r3.control));
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngTemplateOutlet", _r1);
  }
}
function DynamicControlComponent_ng_container_0_div_3_theia_key_value_editor_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](0, "theia-key-value-editor", 10);
  }
  if (rf & 2) {
    const ctx_r17 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("id", ctx_r17.control.id)("parent", ctx_r17.parentForm)("readonly", ctx_r17.readonly)("addLabel", ctx_r17.control.add_value_label)("keyLabel", ctx_r17.control.key_label)("valueLabel", ctx_r17.control.value_label)("value", ctx_r17.keyValueString)("loading", ctx_r17.loadingDataSource);
  }
}
function DynamicControlComponent_ng_container_0_div_3_ng_template_4_Template(rf, ctx) {}
function DynamicControlComponent_ng_container_0_div_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 4)(1, "label", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](3, DynamicControlComponent_ng_container_0_div_3_theia_key_value_editor_3_Template, 1, 8, "theia-key-value-editor", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](4, DynamicControlComponent_ng_container_0_div_3_ng_template_4_Template, 0, 0, "ng-template", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r4 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2);
    const _r1 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵreference"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngClass", ctx_r4.class);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("htmlFor", ctx_r4.control.id);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r4.control.label);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r4.isKeyValueControl(ctx_r4.control));
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngTemplateOutlet", _r1);
  }
}
function DynamicControlComponent_ng_container_0_div_4_input_2_Template(rf, ctx) {
  if (rf & 1) {
    const _r22 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "input", 14);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("blur", function DynamicControlComponent_ng_container_0_div_4_input_2_Template_input_blur_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r22);
      const ctx_r21 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r21.handleBlur());
    })("change", function DynamicControlComponent_ng_container_0_div_4_input_2_Template_input_change_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r22);
      const ctx_r23 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r23.handleToggleChange($event));
    })("ngModelChange", function DynamicControlComponent_ng_container_0_div_4_input_2_Template_input_ngModelChange_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r22);
      const ctx_r24 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r24.value = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r19 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", ctx_r19.value)("id", ctx_r19.control.id)("disabled", ctx_r19.disabled || ctx_r19.readonly)("readonly", ctx_r19.readonly);
  }
}
function DynamicControlComponent_ng_container_0_div_4_ng_template_5_Template(rf, ctx) {}
function DynamicControlComponent_ng_container_0_div_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 4)(1, "div", 11);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](2, DynamicControlComponent_ng_container_0_div_4_input_2_Template, 1, 4, "input", 12);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](3, "label", 13);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](5, DynamicControlComponent_ng_container_0_div_4_ng_template_5_Template, 0, 0, "ng-template", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r5 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2);
    const _r1 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵreference"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngClass", ctx_r5.class);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r5.isToggle(ctx_r5.control));
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("htmlFor", ctx_r5.control.id);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r5.control.label);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngTemplateOutlet", _r1);
  }
}
function DynamicControlComponent_ng_container_0_div_5_ng_container_3_ng_select_1_Template(rf, ctx) {
  if (rf & 1) {
    const _r29 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "ng-select", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("blur", function DynamicControlComponent_ng_container_0_div_5_ng_container_3_ng_select_1_Template_ng_select_blur_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r29);
      const ctx_r28 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](4);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r28.handleBlur());
    })("ngModelChange", function DynamicControlComponent_ng_container_0_div_5_ng_container_3_ng_select_1_Template_ng_select_ngModelChange_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r29);
      const ctx_r30 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](4);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r30.handleSelectChange($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r27 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("items", ctx_r27.control.options)("id", ctx_r27.control.id)("disabled", ctx_r27.disabled)("compareWith", ctx_r27.compare)("readonly", ctx_r27.readonly)("ngModel", ctx_r27.value);
  }
}
function DynamicControlComponent_ng_container_0_div_5_ng_container_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](1, DynamicControlComponent_ng_container_0_div_5_ng_container_3_ng_select_1_Template, 1, 6, "ng-select", 15);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r25 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r25.control.options);
  }
}
function DynamicControlComponent_ng_container_0_div_5_ng_template_4_Template(rf, ctx) {}
function DynamicControlComponent_ng_container_0_div_5_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 4)(1, "label", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](3, DynamicControlComponent_ng_container_0_div_5_ng_container_3_Template, 2, 1, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](4, DynamicControlComponent_ng_container_0_div_5_ng_template_4_Template, 0, 0, "ng-template", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2);
    const _r1 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵreference"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngClass", ctx_r6.class);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("htmlFor", ctx_r6.control.id);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r6.control.label);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r6.isSelect(ctx_r6.control));
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngTemplateOutlet", _r1);
  }
}
function DynamicControlComponent_ng_container_0_div_6_ng_container_3_ng_select_1_ng_template_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](0, "input", 21);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](1, " All ");
  }
  if (rf & 2) {
    const item$_r37 = ctx.item$;
    const index_r38 = ctx.index;
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpropertyInterpolate1"]("id", "item-", index_r38, "-all");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", item$_r37.selected);
  }
}
function DynamicControlComponent_ng_container_0_div_6_ng_container_3_ng_select_1_ng_template_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](0, "input", 21);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](1);
  }
  if (rf & 2) {
    const item_r39 = ctx.item;
    const item$_r40 = ctx.item$;
    const index_r41 = ctx.index;
    const ctx_r35 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpropertyInterpolate1"]("id", "item-", index_r41, "");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", item$_r40.selected);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵattribute"]("checked", ctx_r35.allSelected);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate1"](" ", item_r39.label, " ");
  }
}
function DynamicControlComponent_ng_container_0_div_6_ng_container_3_ng_select_1_Template(rf, ctx) {
  if (rf & 1) {
    const _r43 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "ng-select", 18);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("blur", function DynamicControlComponent_ng_container_0_div_6_ng_container_3_ng_select_1_Template_ng_select_blur_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r43);
      const ctx_r42 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](4);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r42.handleBlur());
    })("ngModelChange", function DynamicControlComponent_ng_container_0_div_6_ng_container_3_ng_select_1_Template_ng_select_ngModelChange_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r43);
      const ctx_r44 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](4);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r44.handleSelectChange($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](1, DynamicControlComponent_ng_container_0_div_6_ng_container_3_ng_select_1_ng_template_1_Template, 2, 2, "ng-template", 19);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](2, DynamicControlComponent_ng_container_0_div_6_ng_container_3_ng_select_1_ng_template_2_Template, 2, 4, "ng-template", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r33 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("items", ctx_r33.control.options)("multiple", true)("selectableGroup", true)("selectableGroupAsModel", false)("closeOnSelect", false)("id", ctx_r33.control.id)("disabled", ctx_r33.disabled)("compareWith", ctx_r33.compare)("readonly", ctx_r33.readonly)("ngModel", ctx_r33.value);
  }
}
function DynamicControlComponent_ng_container_0_div_6_ng_container_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](1, DynamicControlComponent_ng_container_0_div_6_ng_container_3_ng_select_1_Template, 3, 10, "ng-select", 17);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r31 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r31.control.options);
  }
}
function DynamicControlComponent_ng_container_0_div_6_ng_template_4_Template(rf, ctx) {}
function DynamicControlComponent_ng_container_0_div_6_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 4)(1, "label", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](3, DynamicControlComponent_ng_container_0_div_6_ng_container_3_Template, 2, 1, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](4, DynamicControlComponent_ng_container_0_div_6_ng_template_4_Template, 0, 0, "ng-template", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2);
    const _r1 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵreference"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngClass", ctx_r7.class);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("htmlFor", ctx_r7.control.id);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r7.control.label);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r7.isMultiSelect(ctx_r7.control));
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngTemplateOutlet", _r1);
  }
}
function DynamicControlComponent_ng_container_0_div_7_ng_container_1_ng_template_4_Template(rf, ctx) {}
function DynamicControlComponent_ng_container_0_div_7_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    const _r48 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](1, "label", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](3, "textarea", 22);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("blur", function DynamicControlComponent_ng_container_0_div_7_ng_container_1_Template_textarea_blur_3_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r48);
      const ctx_r47 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r47.handleBlur());
    })("input", function DynamicControlComponent_ng_container_0_div_7_ng_container_1_Template_textarea_input_3_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r48);
      const ctx_r49 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r49.handleInput($event));
    })("ngModelChange", function DynamicControlComponent_ng_container_0_div_7_ng_container_1_Template_textarea_ngModelChange_3_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r48);
      const ctx_r50 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r50.value = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](4, DynamicControlComponent_ng_container_0_div_7_ng_container_1_ng_template_4_Template, 0, 0, "ng-template", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r45 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
    const _r1 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵreference"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("htmlFor", ctx_r45.control.id);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r45.control.label);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", ctx_r45.value)("disabled", ctx_r45.disabled)("id", ctx_r45.control.id)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpureFunction1"](10, _c0, ctx_r45.invalid))("theiaControlAttributes", ctx_r45.control.attributes)("readonly", ctx_r45.readonly);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵattribute"]("aria-described-by", ctx_r45.control.id + "Help");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngTemplateOutlet", _r1);
  }
}
function DynamicControlComponent_ng_container_0_div_7_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](1, DynamicControlComponent_ng_container_0_div_7_ng_container_1_Template, 5, 12, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r8 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngClass", ctx_r8.class);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r8.isTextArea(ctx_r8.control));
  }
}
const _c1 = function () {
  return {
    clipboard: true
  };
};
function DynamicControlComponent_ng_container_0_div_8_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    const _r53 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](1, "label", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](3, "input", 23);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("ngModelChange", function DynamicControlComponent_ng_container_0_div_8_ng_container_1_Template_input_ngModelChange_3_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r53);
      const ctx_r52 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r52.value = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](4, "div", 24);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipe"](5, "markdown");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipe"](6, "language");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r51 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("htmlFor", ctx_r51.control.id);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r51.control.label);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", ctx_r51.value)("id", ctx_r51.control.id);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("innerHTML", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipeBind2"](5, 5, _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipeBind2"](6, 8, ctx_r51.valueAsString, ctx_r51.control.language || "json"), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpureFunction0"](11, _c1)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵsanitizeHtml"]);
  }
}
function DynamicControlComponent_ng_container_0_div_8_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](1, DynamicControlComponent_ng_container_0_div_8_ng_container_1_Template, 7, 12, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r9 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngClass", ctx_r9.class);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r9.isCodeControl(ctx_r9.control));
  }
}
function DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_i_7_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](0, "i", 43);
  }
}
function DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_i_8_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](0, "i", 44);
  }
}
function DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_div_9_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](0, "div", 45);
  }
}
function DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_button_14_Template(rf, ctx) {
  if (rf & 1) {
    const _r69 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "button", 46);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("click", function DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_button_14_Template_button_click_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r69);
      const item_r60 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]().$implicit;
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](item_r60.cancel());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](1, "i", 47);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
}
function DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_ng_template_15_ng_container_0_Template(rf, ctx) {
  if (rf & 1) {
    const _r73 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](1, "button", 48);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("click", function DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_ng_template_15_ng_container_0_Template_button_click_1_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r73);
      const item_r60 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2).$implicit;
      const ctx_r71 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](5);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r71.uploadFile(item_r60));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](2, "i", 49);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](3, "button", 50);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("click", function DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_ng_template_15_ng_container_0_Template_button_click_3_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r73);
      const item_r60 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2).$implicit;
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](item_r60.remove());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](4, "i", 51);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
}
function DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_ng_template_15_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](0, DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_ng_template_15_ng_container_0_Template, 5, 0, "ng-container", 0);
  }
  if (rf & 2) {
    const item_r60 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]().$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", !item_r60.isSuccess);
  }
}
const _c2 = function (a0) {
  return {
    width: a0
  };
};
function DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "tr", 32)(1, "td", 33);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](3, "td");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipe"](5, "fileSize");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](6, "td", 34);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](7, DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_i_7_Template, 1, 0, "i", 35);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](8, DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_i_8_Template, 1, 0, "i", 36);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](9, DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_div_9_Template, 1, 0, "div", 37);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](10, "td", 38)(11, "div", 39);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](12, "div", 40);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](13, "td");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](14, DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_button_14_Template, 2, 0, "button", 41);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](15, DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_ng_template_15_Template, 1, 1, "ng-template", null, 42, _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplateRefExtractor"]);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const item_r60 = ctx.$implicit;
    const _r65 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵreference"](16);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("title", item_r60 == null ? null : item_r60.file == null ? null : item_r60.file.name);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](item_r60 == null ? null : item_r60.file == null ? null : item_r60.file.name);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpipeBind1"](5, 9, item_r60 == null ? null : item_r60.file == null ? null : item_r60.file.size));
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", item_r60.isError);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", item_r60.isSuccess);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", item_r60.isUploading);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngStyle", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpureFunction1"](11, _c2, item_r60.progress + "%"));
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", item_r60.isUploading)("ngIfElse", _r65);
  }
}
function DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tfoot_15_Template(rf, ctx) {
  if (rf & 1) {
    const _r78 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "tfoot")(1, "tr")(2, "td", 52)(3, "button", 53);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("click", function DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tfoot_15_Template_button_click_3_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r78);
      const ctx_r77 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](5);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r77.uploadAll());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](4, "Upload all");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()()();
  }
}
function DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "table", 28)(1, "thead")(2, "tr", 29)(3, "th");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](4, "File Name");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](5, "th");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](6, "File Size");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](7, "th");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](8, "Status");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](9, "th");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](10, "Progress");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](11, "th");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](12, "Actions");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](13, "tbody", 30);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](14, DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tr_14_Template, 17, 13, "tr", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](15, DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_tfoot_15_Template, 5, 0, "tfoot", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r55 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](14);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngForOf", ctx_r55.uploader == null ? null : ctx_r55.uploader.queue);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", !ctx_r55.allUploaded() && ctx_r55.isUploadControl(ctx_r55.control) && ctx_r55.control.multiple);
  }
}
const _c3 = function (a0) {
  return {
    "drop-zone-over": a0
  };
};
function DynamicControlComponent_ng_container_0_div_9_ng_container_1_ng_container_5_Template(rf, ctx) {
  if (rf & 1) {
    const _r80 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](1, "div", 54);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("fileOver", function DynamicControlComponent_ng_container_0_div_9_ng_container_1_ng_container_5_Template_div_fileOver_1_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵrestoreView"](_r80);
      const ctx_r79 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](4);
      return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵresetView"](ctx_r79.fileOver($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](2, "div", 55);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](3, "img", 56);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](4, "div", 57)(5, "label", 58);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](6, "Click to upload ");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](7, " or drag and drop ");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](8, "input", 59);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r56 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("uploader", ctx_r56.uploader)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵpureFunction1"](4, _c3, ctx_r56.dropZoneOver));
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](7);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("uploader", ctx_r56.uploader)("multiple", ctx_r56.control.multiple);
  }
}
function DynamicControlComponent_ng_container_0_div_9_ng_container_1_ng_template_6_Template(rf, ctx) {}
function DynamicControlComponent_ng_container_0_div_9_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](1, "label", 25);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](3, "div", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](4, DynamicControlComponent_ng_container_0_div_9_ng_container_1_table_4_Template, 16, 2, "table", 27);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](5, DynamicControlComponent_ng_container_0_div_9_ng_container_1_ng_container_5_Template, 9, 6, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](6, DynamicControlComponent_ng_container_0_div_9_ng_container_1_ng_template_6_Template, 0, 0, "ng-template", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r54 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
    const _r1 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵreference"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r54.control.label);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r54.uploader == null ? null : ctx_r54.uploader.queue == null ? null : ctx_r54.uploader.queue.length);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r54.isUploadControl(ctx_r54.control) && (ctx_r54.control.multiple || !ctx_r54.control.multiple && ctx_r54.uploaderItems < 1));
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngTemplateOutlet", _r1);
  }
}
function DynamicControlComponent_ng_container_0_div_9_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](1, DynamicControlComponent_ng_container_0_div_9_ng_container_1_Template, 7, 4, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r10 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngClass", ctx_r10.class);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r10.isUploadControl(ctx_r10.control));
  }
}
function DynamicControlComponent_ng_container_0_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0)(1, 2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](2, DynamicControlComponent_ng_container_0_div_2_Template, 5, 5, "div", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](3, DynamicControlComponent_ng_container_0_div_3_Template, 5, 5, "div", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](4, DynamicControlComponent_ng_container_0_div_4_Template, 6, 5, "div", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](5, DynamicControlComponent_ng_container_0_div_5_Template, 5, 5, "div", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](6, DynamicControlComponent_ng_container_0_div_6_Template, 5, 5, "div", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](7, DynamicControlComponent_ng_container_0_div_7_Template, 2, 2, "div", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](8, DynamicControlComponent_ng_container_0_div_8_Template, 2, 2, "div", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](9, DynamicControlComponent_ng_container_0_div_9_Template, 2, 2, "div", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]()();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngSwitch", ctx_r0.control.type);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngSwitchCase", ctx_r0.TheiaControl.Input);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngSwitchCase", ctx_r0.TheiaControl.KeyValue);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngSwitchCase", ctx_r0.TheiaControl.Toggle);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngSwitchCase", ctx_r0.TheiaControl.Select);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngSwitchCase", ctx_r0.TheiaControl.MultiSelect);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngSwitchCase", ctx_r0.TheiaControl.TextArea);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngSwitchCase", ctx_r0.TheiaControl.Code);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngSwitchCase", ctx_r0.TheiaControl.Upload);
  }
}
function DynamicControlComponent_ng_template_1_ng_container_0_small_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "small", 62);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r82 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("id", ctx_r82.control.id + "Help");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](ctx_r82.control.help);
  }
}
function DynamicControlComponent_ng_template_1_ng_container_0_div_2_ng_container_2_li_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "li");
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const error_r85 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]().$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate"](error_r85);
  }
}
function DynamicControlComponent_ng_template_1_ng_container_0_div_2_ng_container_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](1, DynamicControlComponent_ng_template_1_ng_container_0_div_2_ng_container_2_li_1_Template, 2, 1, "li", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const error_r85 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", error_r85);
  }
}
function DynamicControlComponent_ng_template_1_ng_container_0_div_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 63)(1, "ul", 64);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](2, DynamicControlComponent_ng_template_1_ng_container_0_div_2_ng_container_2_Template, 2, 1, "ng-container", 65);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r83 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngForOf", ctx_r83.validationErrors);
  }
}
function DynamicControlComponent_ng_template_1_ng_container_0_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](1, DynamicControlComponent_ng_template_1_ng_container_0_small_1_Template, 2, 2, "small", 60);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](2, DynamicControlComponent_ng_template_1_ng_container_0_div_2_Template, 3, 1, "div", 61);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r81 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", !ctx_r81.invalid);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r81.invalid);
  }
}
function DynamicControlComponent_ng_template_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](0, DynamicControlComponent_ng_template_1_ng_container_0_Template, 3, 2, "ng-container", 0);
  }
  if (rf & 2) {
    const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx_r2.control);
  }
}
let DynamicControlComponent = /*#__PURE__*/(() => {
  class DynamicControlComponent {
    get valueAsString() {
      return this.value;
    }
    constructor(ngControl, cdr, dataSourceService, commandService, s3UploadService) {
      this.ngControl = ngControl;
      this.cdr = cdr;
      this.dataSourceService = dataSourceService;
      this.commandService = commandService;
      this.s3UploadService = s3UploadService;
      this.datasource = '';
      this.parentForm = new _angular_forms__WEBPACK_IMPORTED_MODULE_2__.UntypedFormGroup({});
      this.class = "";
      this.TheiaControl = _models_template__WEBPACK_IMPORTED_MODULE_3__.TheiaControl;
      this.value = '';
      this.isDisabled = false;
      this.allSelected = false;
      this.keyValueString = '';
      this.loadingDataSource = false;
      this.dropZoneOver = false;
      this.isInputControl = _models_template_control__WEBPACK_IMPORTED_MODULE_4__.isInputControl;
      this.isKeyValueControl = _models_template_control__WEBPACK_IMPORTED_MODULE_4__.isKeyValueControl;
      this.isToggle = _models_template_control__WEBPACK_IMPORTED_MODULE_4__.isToggleControl;
      this.isSelect = _models_template_control__WEBPACK_IMPORTED_MODULE_4__.isSelectControl;
      this.isMultiSelect = _models_template_control__WEBPACK_IMPORTED_MODULE_4__.isMultiSelectControl;
      this.isTextArea = _models_template_control__WEBPACK_IMPORTED_MODULE_4__.isTextAreaControl;
      this.isCodeControl = _models_template_control__WEBPACK_IMPORTED_MODULE_4__.isCodeControl;
      this.isUploadControl = _models_template_control__WEBPACK_IMPORTED_MODULE_4__.isUploadControl;
      this.onChange = _ => {};
      this.onTouch = () => {};
      this.ngControl.valueAccessor = this;
      this.isNew$ = commandService.isNew$;
    }
    get invalid() {
      return !!((this.ngControl.touched || this.ngControl.dirty) && this.ngControl.invalid);
    }
    get disabled() {
      return !!this.ngControl.disabled;
    }
    get readonly() {
      return !!(this.control?.readonly || this.control?.readonly_edit && !this.isNew$.value);
    }
    get validationErrors() {
      const errorTypes = {
        email: _models_template__WEBPACK_IMPORTED_MODULE_5__.TheiaValidation.Email,
        max: _models_template__WEBPACK_IMPORTED_MODULE_5__.TheiaValidation.Max,
        min: _models_template__WEBPACK_IMPORTED_MODULE_5__.TheiaValidation.Min,
        minlength: _models_template__WEBPACK_IMPORTED_MODULE_5__.TheiaValidation.MinLength,
        maxlength: _models_template__WEBPACK_IMPORTED_MODULE_5__.TheiaValidation.MaxLength,
        pattern: _models_template__WEBPACK_IMPORTED_MODULE_5__.TheiaValidation.Pattern,
        required: _models_template__WEBPACK_IMPORTED_MODULE_5__.TheiaValidation.Required,
        requiredtrue: _models_template__WEBPACK_IMPORTED_MODULE_5__.TheiaValidation.RequiredTrue
      };
      return Object.keys(this.ngControl.errors).map(errorCode => {
        const validation = this.findValidationByType(errorTypes[errorCode]);
        return validation?.message || '';
      });
    }
    get uploaderItems() {
      return this.uploader?.queue.length || 0;
    }
    ngOnInit() {
      if (!this.datasource && (0,_models_template_control__WEBPACK_IMPORTED_MODULE_4__.isSelectOrMultiSelect)(this.control)) {
        (this.control || {}).options = this.groupIfMultiSelect(this.control?.options || []);
      }
    }
    ngOnChanges(changes) {
      if (changes.datasource && changes.datasource.currentValue) {
        if ((0,_models_template_control__WEBPACK_IMPORTED_MODULE_4__.isSelectOrMultiSelect)(this.control) && this.control?.dependency?.datasourceDependency && changes.datasource.firstChange) {
          (this.control || {}).options = [];
        } else if (this.control?.type !== _models_template__WEBPACK_IMPORTED_MODULE_3__.TheiaControl.Upload) {
          this.loadDatasource(changes.datasource.currentValue);
        }
      }
    }
    writeValue(value) {
      if (this.control?.type === _models_template__WEBPACK_IMPORTED_MODULE_3__.TheiaControl.MultiSelect && typeof value === 'string') {
        value = value.split(',');
      }
      if (this.control?.type === _models_template__WEBPACK_IMPORTED_MODULE_3__.TheiaControl.Upload) {
        const options = {
          disableMultipart: true,
          method: 'PUT',
          url: ''
        };
        if (!this.control?.multiple) {
          options.queueLimit = 1;
        }
        this.uploader = new ng2_file_upload__WEBPACK_IMPORTED_MODULE_6__.FileUploader(options);
        this.uploader.onSuccessItem = this.handleUploadSuccess.bind(this);
      }
      this.value = value;
      this.cdr.detectChanges();
    }
    registerOnChange(fn) {
      this.onChange = fn;
    }
    registerOnTouched(fn) {
      this.onTouch = fn;
    }
    setDisabledState(isDisabled) {
      this.isDisabled = isDisabled;
    }
    handleInput(event) {
      this.value = event.target.value;
      this.onTouch();
      this.onChange(this.value);
    }
    findValidationByType(type) {
      if ((0,_models_template_control__WEBPACK_IMPORTED_MODULE_4__.isComplexControl)(this.control)) {
        return;
      }
      return this.control?.validations?.find(validation => validation.type === type);
    }
    handleToggleChange(event) {
      this.value = event.target.checked;
      this.onTouch();
      this.onChange(this.value);
    }
    handleBlur() {
      this.onTouch();
    }
    handleSelectChange(value) {
      this.value = value;
      this.onTouch();
      this.onChange(this.value);
    }
    compare(item, selected) {
      if (typeof item.value === 'string') {
        return item.value === selected;
      } else if (item.value) {
        return item.value.value === selected;
      }
      return false;
    }
    groupIfMultiSelect(options = []) {
      if (this.control?.type === _models_template__WEBPACK_IMPORTED_MODULE_3__.TheiaControl.MultiSelect) {
        if (!Array.isArray(options)) {
          options = [];
        }
        return options.map(option => {
          option.theiaSelectAll = 'all';
          return option;
        });
      }
      return options;
    }
    loadDatasource(datasource) {
      if (!(0,_models_template_control__WEBPACK_IMPORTED_MODULE_4__.hasDatasource)(this.control)) {
        return;
      }
      this.loadingDataSource = true;
      this.dataSourceService.getData(datasource, !this.control?.env_not_required).subscribe(response => {
        const control = this.control || {};
        switch (this.control?.type) {
          case _models_template__WEBPACK_IMPORTED_MODULE_3__.TheiaControl.MultiSelect:
          case _models_template__WEBPACK_IMPORTED_MODULE_3__.TheiaControl.Select:
            control.options = this.groupIfMultiSelect(response);
            break;
          case _models_template__WEBPACK_IMPORTED_MODULE_3__.TheiaControl.KeyValue:
            this.value = '';
            this.keyValueString = '';
            this.cdr.detectChanges();
            this.value = JSON.stringify(response);
            this.keyValueString = this.value;
            break;
          default:
            break;
        }
        this.loadingDataSource = false;
      }, () => this.loadingDataSource = false);
    }
    fileOver(event) {
      this.dropZoneOver = event;
    }
    uploadFile(fileItem) {
      if (this.control?.type === _models_template__WEBPACK_IMPORTED_MODULE_3__.TheiaControl.Upload) {
        fileItem.isError = false;
        const fileType = mime__WEBPACK_IMPORTED_MODULE_0__.getType(fileItem.file.name || '') || 'application/octet-stream';
        this.s3UploadService.getSignedUrl(this.control?.datasource, fileType, fileItem.file.name).subscribe(response => {
          if (!response.length) {
            fileItem.isError = true;
            return;
          }
          fileItem.url = response[0].presigned_url;
          const additionalHeaders = Object.entries(this.control?.type === _models_template__WEBPACK_IMPORTED_MODULE_3__.TheiaControl.Upload && this.control?.metadata || {}).map(([name, value]) => ({
            name: `x-amz-meta-${name}`,
            value
          }));
          fileItem.headers = [{
            name: "Content-Type",
            value: fileType
          }, ...additionalHeaders];
          fileItem.upload();
        }, error => {
          fileItem.isError = true;
        });
      }
    }
    uploadAll() {
      for (const fileItem of this.uploader?.queue || []) {
        if (!fileItem.isSuccess) {
          this.uploadFile(fileItem);
        }
      }
    }
    allUploaded() {
      return this.uploader?.queue.every(item => item.isSuccess);
    }
    handleUploadSuccess(item) {
      if (!this.value) {
        this.value = [];
      }
      this.value.push(item.url);
      this.onChange(this.value);
    }
    static #_ = this.ɵfac = function DynamicControlComponent_Factory(t) {
      return new (t || DynamicControlComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_angular_forms__WEBPACK_IMPORTED_MODULE_2__.NgControl, 10), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_1__.ChangeDetectorRef), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_data_source_service__WEBPACK_IMPORTED_MODULE_7__.DataSourceService), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_command_service__WEBPACK_IMPORTED_MODULE_8__.CommandService), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_services_s3_upload_service__WEBPACK_IMPORTED_MODULE_9__.S3UploadService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineComponent"]({
      type: DynamicControlComponent,
      selectors: [["theia-dynamic-control"]],
      inputs: {
        control: "control",
        datasource: "datasource",
        parentForm: "parentForm",
        step: "step",
        class: "class"
      },
      features: [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵNgOnChangesFeature"]],
      decls: 3,
      vars: 1,
      consts: [[4, "ngIf"], ["controlFeedback", ""], [3, "ngSwitch"], [3, "ngClass", 4, "ngSwitchCase"], [3, "ngClass"], [1, "form-label", 3, "htmlFor"], ["class", "form-control", 3, "ngModel", "disabled", "id", "ngClass", "theiaControlAttributes", "type", "readonly", "blur", "input", "ngModelChange", 4, "ngIf"], [3, "ngTemplateOutlet"], [1, "form-control", 3, "ngModel", "disabled", "id", "ngClass", "theiaControlAttributes", "type", "readonly", "blur", "input", "ngModelChange"], [3, "id", "parent", "readonly", "addLabel", "keyLabel", "valueLabel", "value", "loading", 4, "ngIf"], [3, "id", "parent", "readonly", "addLabel", "keyLabel", "valueLabel", "value", "loading"], [1, "form-check", "form-switch"], ["class", "form-check-input", "type", "checkbox", 3, "ngModel", "id", "disabled", "readonly", "blur", "change", "ngModelChange", 4, "ngIf"], [1, "form-check-label", 3, "htmlFor"], ["type", "checkbox", 1, "form-check-input", 3, "ngModel", "id", "disabled", "readonly", "blur", "change", "ngModelChange"], ["bindValue", "value", 3, "items", "id", "disabled", "compareWith", "readonly", "ngModel", "blur", "ngModelChange", 4, "ngIf"], ["bindValue", "value", 3, "items", "id", "disabled", "compareWith", "readonly", "ngModel", "blur", "ngModelChange"], ["groupBy", "theiaSelectAll", "bindValue", "value", 3, "items", "multiple", "selectableGroup", "selectableGroupAsModel", "closeOnSelect", "id", "disabled", "compareWith", "readonly", "ngModel", "blur", "ngModelChange", 4, "ngIf"], ["groupBy", "theiaSelectAll", "bindValue", "value", 3, "items", "multiple", "selectableGroup", "selectableGroupAsModel", "closeOnSelect", "id", "disabled", "compareWith", "readonly", "ngModel", "blur", "ngModelChange"], ["ng-optgroup-tmp", ""], ["ng-option-tmp", ""], ["type", "checkbox", 3, "id", "ngModel"], [1, "form-control", 3, "ngModel", "disabled", "id", "ngClass", "theiaControlAttributes", "readonly", "blur", "input", "ngModelChange"], ["type", "hidden", 1, "form-control", 3, "ngModel", "id", "ngModelChange"], [3, "innerHTML"], [1, "form-label"], [1, "table-responsive"], ["class", "table", 4, "ngIf"], [1, "table"], [2, "white-space", "nowrap"], [1, "upload-table"], ["class", "align-middle", 4, "ngFor", "ngForOf"], [1, "align-middle"], [3, "title"], [1, "text-center"], ["class", "text-danger bi bi-exclamation-triangle", "aria-hidden", "true", 4, "ngIf"], ["class", "text-success bi bi-check", "aria-hidden", "true", 4, "ngIf"], ["class", "spinner-border spinner-border-sm", 4, "ngIf"], [1, "column-progress"], [1, "progress"], ["role", "progressbar", 1, "progress-bar", 3, "ngStyle"], ["type", "button", "class", "btn btn-sm btn-outline-warning me-2", 3, "click", 4, "ngIf", "ngIfElse"], ["notUploading", ""], ["aria-hidden", "true", 1, "text-danger", "bi", "bi-exclamation-triangle"], ["aria-hidden", "true", 1, "text-success", "bi", "bi-check"], [1, "spinner-border", "spinner-border-sm"], ["type", "button", 1, "btn", "btn-sm", "btn-outline-warning", "me-2", 3, "click"], [1, "bi", "bi-x-circle"], ["type", "button", 1, "btn", "btn-sm", "btn-outline-primary", "me-1", 3, "click"], [1, "bi", "bi-cloud-upload"], ["type", "button", 1, "btn", "btn-sm", "btn-outline-danger", 3, "click"], [1, "bi", "bi-trash"], ["colspan", "5", 1, "text-end"], ["type", "button", 1, "btn", "btn-sm", "btn-outline-primary", 3, "click"], ["ng2FileDrop", "", 1, "card", "drop-zone", 3, "uploader", "ngClass", "fileOver"], [1, "card-body", "text-center"], ["ngSrc", "assets/img/upload-cloud-02.svg", "alt", "upload", "height", "20", "width", "20"], [1, "mt-3"], ["for", "attachments", 1, "file-input-label"], ["type", "file", "ng2FileSelect", "", "id", "attachments", 1, "file-input", 3, "uploader", "multiple"], ["class", "form-text text-muted", 3, "id", 4, "ngIf"], ["class", "invalid-feedback", 4, "ngIf"], [1, "form-text", "text-muted", 3, "id"], [1, "invalid-feedback"], [1, "list-unstyled"], [4, "ngFor", "ngForOf"]],
      template: function DynamicControlComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](0, DynamicControlComponent_ng_container_0_Template, 10, 9, "ng-container", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplate"](1, DynamicControlComponent_ng_template_1_Template, 1, 1, "ng-template", null, 1, _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtemplateRefExtractor"]);
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngIf", ctx.control && !ctx.control.hidden);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_10__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_10__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_10__.NgIf, _angular_common__WEBPACK_IMPORTED_MODULE_10__.NgTemplateOutlet, _angular_common__WEBPACK_IMPORTED_MODULE_10__.NgStyle, _angular_common__WEBPACK_IMPORTED_MODULE_10__.NgSwitch, _angular_common__WEBPACK_IMPORTED_MODULE_10__.NgSwitchCase, _angular_forms__WEBPACK_IMPORTED_MODULE_2__.DefaultValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_2__.CheckboxControlValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_2__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_2__.NgModel, _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_11__.NgSelectComponent, _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_11__.NgOptgroupTemplateDirective, _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_11__.NgOptionTemplateDirective, ng2_file_upload__WEBPACK_IMPORTED_MODULE_6__.FileDropDirective, ng2_file_upload__WEBPACK_IMPORTED_MODULE_6__.FileSelectDirective, _angular_common__WEBPACK_IMPORTED_MODULE_10__.NgOptimizedImage, _directives_control_attributes_directive__WEBPACK_IMPORTED_MODULE_12__.ControlAttributesDirective, _key_value_editor_key_value_editor_component__WEBPACK_IMPORTED_MODULE_13__.KeyValueEditorComponent, ngx_markdown__WEBPACK_IMPORTED_MODULE_14__.LanguagePipe, ngx_markdown__WEBPACK_IMPORTED_MODULE_14__.MarkdownPipe, _pipes_file_size_pipe__WEBPACK_IMPORTED_MODULE_15__.FileSizePipe],
      styles: [".ng-dropdown-panel .ng-dropdown-panel-items .ng-option.ng-option-child {\n  padding-left: 10px;\n}\n\n.drop-zone-over[_ngcontent-%COMP%] {\n  border-color: #17a2b8;\n}\n\n.file-input[_ngcontent-%COMP%] {\n  display: none;\n}\n\n.file-input-label[_ngcontent-%COMP%] {\n  color: #007bff;\n  text-decoration: none;\n  background-color: transparent;\n  cursor: pointer;\n}\n\n.file-input-label[_ngcontent-%COMP%]:hover {\n  color: #0056b3;\n  text-decoration: underline;\n}\n\n.upload-table[_ngcontent-%COMP%] {\n  width: 100%;\n}\n.upload-table[_ngcontent-%COMP%]   tr[_ngcontent-%COMP%]   td[_ngcontent-%COMP%] {\n  max-width: 0;\n  white-space: nowrap;\n}\n.upload-table[_ngcontent-%COMP%]   tr[_ngcontent-%COMP%]   td[_ngcontent-%COMP%]:nth-child(1) {\n  text-overflow: ellipsis;\n  overflow: hidden;\n  width: 50%;\n}\n.upload-table[_ngcontent-%COMP%]   tr[_ngcontent-%COMP%]   td[_ngcontent-%COMP%]:nth-child(2) {\n  width: 10%;\n}\n.upload-table[_ngcontent-%COMP%]   tr[_ngcontent-%COMP%]   td[_ngcontent-%COMP%]:nth-child(3) {\n  width: 5%;\n}\n.upload-table[_ngcontent-%COMP%]   tr[_ngcontent-%COMP%]   td[_ngcontent-%COMP%]:nth-child(4) {\n  width: 20%;\n}\n.upload-table[_ngcontent-%COMP%]   tr[_ngcontent-%COMP%]   td[_ngcontent-%COMP%]:nth-child(5) {\n  width: 15%;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9keW5hbWljLWNvbnRyb2wvZHluYW1pYy1jb250cm9sLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUlBO0VBQ0Usa0JBQUE7QUFIRjs7QUFVQTtFQUNFLHFCQUFBO0FBUEY7O0FBVUE7RUFDRSxhQUFBO0FBUEY7O0FBVUE7RUFDRSxjQUFBO0VBQ0EscUJBQUE7RUFDQSw2QkFBQTtFQUNBLGVBQUE7QUFQRjs7QUFVQTtFQUNFLGNBQUE7RUFDQSwwQkFBQTtBQVBGOztBQVVBO0VBQ0UsV0FBQTtBQVBGO0FBU0k7RUFDRSxZQUFBO0VBQ0EsbUJBQUE7QUFQTjtBQVNJO0VBQ0UsdUJBQUE7RUFDQSxnQkFBQTtFQUNBLFVBQUE7QUFQTjtBQVNJO0VBQ0UsVUFBQTtBQVBOO0FBU0k7RUFDRSxTQUFBO0FBUE47QUFTSTtFQUNFLFVBQUE7QUFQTjtBQVNJO0VBQ0UsVUFBQTtBQVBOIiwic291cmNlc0NvbnRlbnQiOlsiLm5nLXNlbGVjdCA6Om5nLWRlZXAge1xuXG59XG5cbjo6bmctZGVlcCAubmctZHJvcGRvd24tcGFuZWwgLm5nLWRyb3Bkb3duLXBhbmVsLWl0ZW1zIC5uZy1vcHRpb24ubmctb3B0aW9uLWNoaWxkIHtcbiAgcGFkZGluZy1sZWZ0OiAxMHB4O1xufVxuXG4uZHJvcC16b25lIHtcblxufVxuXG4uZHJvcC16b25lLW92ZXIge1xuICBib3JkZXItY29sb3I6ICMxN2EyYjg7XG59XG5cbi5maWxlLWlucHV0IHtcbiAgZGlzcGxheTogbm9uZTtcbn1cblxuLmZpbGUtaW5wdXQtbGFiZWwge1xuICBjb2xvcjogIzAwN2JmZjtcbiAgdGV4dC1kZWNvcmF0aW9uOiBub25lO1xuICBiYWNrZ3JvdW5kLWNvbG9yOiB0cmFuc3BhcmVudDtcbiAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG4uZmlsZS1pbnB1dC1sYWJlbDpob3ZlciB7XG4gIGNvbG9yOiAjMDA1NmIzO1xuICB0ZXh0LWRlY29yYXRpb246IHVuZGVybGluZTtcbn1cblxuLnVwbG9hZC10YWJsZSB7XG4gIHdpZHRoOiAxMDAlO1xuICB0ciB7XG4gICAgdGQge1xuICAgICAgbWF4LXdpZHRoOiAwO1xuICAgICAgd2hpdGUtc3BhY2U6IG5vd3JhcDtcbiAgICB9XG4gICAgdGQ6bnRoLWNoaWxkKDEpIHtcbiAgICAgIHRleHQtb3ZlcmZsb3c6IGVsbGlwc2lzO1xuICAgICAgb3ZlcmZsb3c6IGhpZGRlbjtcbiAgICAgIHdpZHRoOiA1MCU7XG4gICAgfVxuICAgIHRkOm50aC1jaGlsZCgyKSB7XG4gICAgICB3aWR0aDogMTAlO1xuICAgIH1cbiAgICB0ZDpudGgtY2hpbGQoMykge1xuICAgICAgd2lkdGg6IDUlO1xuICAgIH1cbiAgICB0ZDpudGgtY2hpbGQoNCkge1xuICAgICAgd2lkdGg6IDIwJTtcbiAgICB9XG4gICAgdGQ6bnRoLWNoaWxkKDUpIHtcbiAgICAgIHdpZHRoOiAxNSU7XG4gICAgfVxuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9 */"]
    });
  }
  return DynamicControlComponent;
})();

/***/ }),

/***/ 3439:
/*!*******************************************************************!*\
  !*** ./src/app/components/dynamic-form/dynamic-form.component.ts ***!
  \*******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DynamicFormComponent: () => (/* binding */ DynamicFormComponent)
/* harmony export */ });
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../models/template */ 7044);
/* harmony import */ var _models_template_control__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../models/template/control */ 6347);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ 8849);
/* harmony import */ var _services_command_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/command.service */ 9167);
/* harmony import */ var _services_window_ref_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/window-ref.service */ 6889);
/* harmony import */ var _services_info_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/info.service */ 957);
/* harmony import */ var _services_data_source_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../services/data-source.service */ 6678);
/* harmony import */ var _services_dynamic_form_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../services/dynamic-form.service */ 449);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var ngx_markdown__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ngx-markdown */ 1995);
/* harmony import */ var _accordion_components_accordion_accordion_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../accordion/components/accordion/accordion.component */ 1638);
/* harmony import */ var _accordion_components_accordion_item_accordion_item_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../accordion/components/accordion-item/accordion-item.component */ 2836);
/* harmony import */ var _dynamic_control_dynamic_control_component__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../dynamic-control/dynamic-control.component */ 1081);
/* harmony import */ var _composite_group_composite_group_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ../composite-group/composite-group.component */ 2096);















function DynamicFormComponent_ng_container_0_div_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 3)(1, "div", 4)(2, "h3");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
  }
  if (rf & 2) {
    const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](ctx_r1.step.title);
  }
}
function DynamicFormComponent_ng_container_0_div_2_markdown_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "markdown", 8);
  }
  if (rf & 2) {
    const ctx_r4 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("data", ctx_r4.step.description);
  }
}
function DynamicFormComponent_ng_container_0_div_2_p_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "p", 9);
  }
  if (rf & 2) {
    const ctx_r5 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("innerHTML", ctx_r5.step.description, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsanitizeHtml"]);
  }
}
function DynamicFormComponent_ng_container_0_div_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 3)(1, "div", 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, DynamicFormComponent_ng_container_0_div_2_markdown_2_Template, 1, 1, "markdown", 6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, DynamicFormComponent_ng_container_0_div_2_p_3_Template, 1, 1, "p", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r2.step.allowMarkdown);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !ctx_r2.step.allowMarkdown);
  }
}
function DynamicFormComponent_ng_container_0_div_5_theia_dynamic_control_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "theia-dynamic-control", 14);
  }
  if (rf & 2) {
    const control_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("control", control_r6)("datasource", control_r6.datasource)("formControlName", control_r6.id)("parentForm", ctx_r7.formGroup)("step", ctx_r7.step);
  }
}
function DynamicFormComponent_ng_container_0_div_5_ng_container_3_theia_accordion_item_2_ng_container_5_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "theia-dynamic-control", 14, 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const item_r15 = ctx.$implicit;
    const ctx_r14 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("control", item_r15)("datasource", item_r15.datasource)("formControlName", item_r15.id)("parentForm", ctx_r14.formGroup)("step", ctx_r14.step);
  }
}
function DynamicFormComponent_ng_container_0_div_5_ng_container_3_theia_accordion_item_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "theia-accordion-item");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](1, 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](2, "theia-dynamic-control", 17, 18);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](4, 19);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](5, DynamicFormComponent_ng_container_0_div_5_ng_container_3_theia_accordion_item_2_ng_container_5_Template, 3, 5, "ng-container", 15);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const module_r12 = ctx.$implicit;
    const ctx_r11 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("control", module_r12)("formControlName", module_r12.id)("parentForm", ctx_r11.formGroup)("step", ctx_r11.step);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", module_r12.controls);
  }
}
function DynamicFormComponent_ng_container_0_div_5_ng_container_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "theia-accordion");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, DynamicFormComponent_ng_container_0_div_5_ng_container_3_theia_accordion_item_2_Template, 6, 5, "theia-accordion-item", 15);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const control_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", control_r6.modules);
  }
}
function DynamicFormComponent_ng_container_0_div_5_theia_composite_group_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "theia-composite-group", 21);
  }
  if (rf & 2) {
    const control_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    const ctx_r9 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("group", ctx_r9.toCompositeControl(control_r6))("parentForm", ctx_r9.formGroup)("step", ctx_r9.step)("id", ctx_r9.selectedId);
  }
}
const _c0 = function (a0) {
  return {
    "d-none": a0
  };
};
function DynamicFormComponent_ng_container_0_div_5_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 10);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](1, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, DynamicFormComponent_ng_container_0_div_5_theia_dynamic_control_2_Template, 1, 5, "theia-dynamic-control", 11);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, DynamicFormComponent_ng_container_0_div_5_ng_container_3_Template, 3, 1, "ng-container", 12);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, DynamicFormComponent_ng_container_0_div_5_theia_composite_group_4_Template, 1, 4, "theia-composite-group", 13);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const control_r6 = ctx.$implicit;
    const ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](6, _c0, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](1, 4, ctx_r3.isNew$) === true && control_r6.new_hide === true));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !ctx_r3.isCompositeModuleControl(control_r6) && !ctx_r3.isCompositeGroupControl(control_r6));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r3.isCompositeModuleControl(control_r6));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r3.isCompositeGroupControl(control_r6));
  }
}
function DynamicFormComponent_ng_container_0_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0, 1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, DynamicFormComponent_ng_container_0_div_1_Template, 4, 1, "div", 2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, DynamicFormComponent_ng_container_0_div_2_Template, 4, 2, "div", 2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "div", 3)(4, "div", 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](5, DynamicFormComponent_ng_container_0_div_5_Template, 5, 8, "div", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formGroup", ctx_r0.formGroup);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r0.step.title);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r0.step.description);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r0.controls);
  }
}
let DynamicFormComponent = /*#__PURE__*/(() => {
  class DynamicFormComponent {
    constructor(fb, commandService, windowRef, infoService, dataSourceService, formService, cdr) {
      this.fb = fb;
      this.commandService = commandService;
      this.windowRef = windowRef;
      this.infoService = infoService;
      this.dataSourceService = dataSourceService;
      this.formService = formService;
      this.cdr = cdr;
      this.selectedId = "";
      this.TheiaControl = _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaControl;
      this.isCompositeModuleControl = _models_template_control__WEBPACK_IMPORTED_MODULE_2__.isCompositeModuleControl;
      this.isCompositeGroupControl = _models_template_control__WEBPACK_IMPORTED_MODULE_2__.isCompositeGroupControl;
      this.isInputControl = _models_template_control__WEBPACK_IMPORTED_MODULE_2__.isInputControl;
      this.formGroup = fb.group({});
      this.window = windowRef.nativeWindow;
      this.isNew$ = commandService.isNew$;
    }
    get controls() {
      if (!this.step) {
        return undefined;
      }
      return this.step.controls;
    }
    ngOnInit() {
      const options = {
        datasource: this.step?.datasource,
        env_param_required: this.step?.env_param_required,
        readonly: this.step?.readonly
      };
      this.formService.initialize(this.formGroup, this.step?.controls || [], this.cdr, options);
    }
    showInfo() {
      this.infoService.showInfoPanel(this.step?.info || '');
    }
    toCompositeControl(control) {
      return control;
    }
    static #_ = this.ɵfac = function DynamicFormComponent_Factory(t) {
      return new (t || DynamicFormComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_forms__WEBPACK_IMPORTED_MODULE_3__.UntypedFormBuilder), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_command_service__WEBPACK_IMPORTED_MODULE_4__.CommandService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_window_ref_service__WEBPACK_IMPORTED_MODULE_5__.WindowRefService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_info_service__WEBPACK_IMPORTED_MODULE_6__.InfoService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_data_source_service__WEBPACK_IMPORTED_MODULE_7__.DataSourceService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_dynamic_form_service__WEBPACK_IMPORTED_MODULE_8__.DynamicFormService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.ChangeDetectorRef));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: DynamicFormComponent,
      selectors: [["theia-dynamic-form"]],
      inputs: {
        step: "step",
        formGroup: "formGroup",
        selectedId: "selectedId"
      },
      decls: 1,
      vars: 1,
      consts: [[3, "formGroup", 4, "ngIf"], [3, "formGroup"], ["class", "row", 4, "ngIf"], [1, "row"], [1, "col"], [3, "ngClass", 4, "ngFor", "ngForOf"], [3, "data", 4, "ngIf"], [3, "innerHTML", 4, "ngIf"], [3, "data"], [3, "innerHTML"], [3, "ngClass"], ["class", "mb-3", 3, "control", "datasource", "formControlName", "parentForm", "step", 4, "ngIf"], [4, "ngIf"], [3, "group", "parentForm", "step", "id", 4, "ngIf"], [1, "mb-3", 3, "control", "datasource", "formControlName", "parentForm", "step"], [4, "ngFor", "ngForOf"], ["slot", "header"], [3, "control", "formControlName", "parentForm", "step"], ["accordionHeader", ""], ["slot", "body"], ["accordionControl", ""], [3, "group", "parentForm", "step", "id"]],
      template: function DynamicFormComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](0, DynamicFormComponent_ng_container_0_Template, 6, 4, "ng-container", 0);
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.step);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_9__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_9__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_9__.NgIf, _angular_forms__WEBPACK_IMPORTED_MODULE_3__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_3__.NgControlStatusGroup, _angular_forms__WEBPACK_IMPORTED_MODULE_3__.FormGroupDirective, _angular_forms__WEBPACK_IMPORTED_MODULE_3__.FormControlName, ngx_markdown__WEBPACK_IMPORTED_MODULE_10__.MarkdownComponent, _accordion_components_accordion_accordion_component__WEBPACK_IMPORTED_MODULE_11__.AccordionComponent, _accordion_components_accordion_item_accordion_item_component__WEBPACK_IMPORTED_MODULE_12__.AccordionItemComponent, _dynamic_control_dynamic_control_component__WEBPACK_IMPORTED_MODULE_13__.DynamicControlComponent, _composite_group_composite_group_component__WEBPACK_IMPORTED_MODULE_14__.CompositeGroupComponent, _angular_common__WEBPACK_IMPORTED_MODULE_9__.AsyncPipe],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return DynamicFormComponent;
})();

/***/ }),

/***/ 1954:
/*!*************************************************************************!*\
  !*** ./src/app/components/dynamic-section/dynamic-section.component.ts ***!
  \*************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DynamicSectionComponent: () => (/* binding */ DynamicSectionComponent)
/* harmony export */ });
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../models/template */ 9671);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_template_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../services/template.service */ 529);
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ 7947);
/* harmony import */ var _services_environment_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/environment.service */ 1574);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var ngx_markdown__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ngx-markdown */ 1995);
/* harmony import */ var _actions_actions_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../actions/actions.component */ 3494);
/* harmony import */ var _steps_steps_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../steps/steps.component */ 5770);
/* harmony import */ var _layout_layout_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../layout/layout.component */ 2952);










function DynamicSectionComponent_div_3__svg_svg_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "svg", 10);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "path", 11)(2, "path", 12);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
function DynamicSectionComponent_div_3__svg_svg_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "svg", 13);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "path", 14)(2, "path", 15);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
function DynamicSectionComponent_div_3_Template(rf, ctx) {
  if (rf & 1) {
    const _r8 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function DynamicSectionComponent_div_3_Template_div_click_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r8);
      const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r7.toggleCollapse());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, DynamicSectionComponent_div_3__svg_svg_1_Template, 3, 0, "svg", 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, DynamicSectionComponent_div_3__svg_svg_2_Template, 3, 0, "svg", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !ctx_r0.collapsed);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r0.collapsed);
  }
}
function DynamicSectionComponent_theia_actions_4_Template(rf, ctx) {
  if (rf & 1) {
    const _r10 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "theia-actions", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("actionSelected", function DynamicSectionComponent_theia_actions_4_Template_theia_actions_actionSelected_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r10);
      const ctx_r9 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r9.handleActionSelected($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("actions", ctx_r1.actions);
  }
}
const _c0 = function () {
  return [];
};
function DynamicSectionComponent_ng_container_6_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "theia-steps", 17);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("actionId", ctx_r2.currentAction.id)("steps", ctx_r2.currentAction.steps || _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction0"](2, _c0));
  }
}
function DynamicSectionComponent_ng_template_7_markdown_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "markdown", 22);
  }
  if (rf & 2) {
    const ctx_r11 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("data", ctx_r11.section == null ? null : ctx_r11.section.description);
  }
}
function DynamicSectionComponent_ng_template_7_p_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "p", 23);
  }
  if (rf & 2) {
    const ctx_r12 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("innerHTML", ctx_r12.section == null ? null : ctx_r12.section.description, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsanitizeHtml"]);
  }
}
function DynamicSectionComponent_ng_template_7_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 18)(1, "div", 19);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, DynamicSectionComponent_ng_template_7_markdown_2_Template, 1, 1, "markdown", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, DynamicSectionComponent_ng_template_7_p_3_Template, 1, 1, "p", 21);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r4 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r4.section == null ? null : ctx_r4.section.allowMarkdown);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !(ctx_r4.section == null ? null : ctx_r4.section.allowMarkdown));
  }
}
const _c1 = function (a0) {
  return {
    collapsed: a0
  };
};
let DynamicSectionComponent = /*#__PURE__*/(() => {
  class DynamicSectionComponent {
    constructor(templateService, activatedRoute, environmentService, cdr, router) {
      this.templateService = templateService;
      this.activatedRoute = activatedRoute;
      this.environmentService = environmentService;
      this.cdr = cdr;
      this.router = router;
      this.actions = [];
      this.TheiaStep = _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaStep;
      this.collapsed = false;
    }
    ngOnInit() {
      this.activatedRoute.paramMap.subscribe(params => {
        const route = params.get('route') || '';
        this.section = this.templateService.getSectionByRoute(route);
        this.currentAction = undefined;
        if (!this.section) {
          const firstRoute = this.templateService.getFirstRoute();
          this.router.navigate(['/action', firstRoute]);
        } else {
          this.actions = this.section.actions;
        }
      });
      this.environmentService.getCurrentEnvironment().subscribe(() => {
        const action = this.currentAction;
        this.currentAction = undefined;
        this.cdr.detectChanges();
        this.currentAction = action;
      });
    }
    handleActionSelected(action) {
      this.currentAction = action;
    }
    toggleCollapse() {
      this.collapsed = !this.collapsed;
    }
    static #_ = this.ɵfac = function DynamicSectionComponent_Factory(t) {
      return new (t || DynamicSectionComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_template_service__WEBPACK_IMPORTED_MODULE_2__.TemplateService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_router__WEBPACK_IMPORTED_MODULE_3__.ActivatedRoute), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_environment_service__WEBPACK_IMPORTED_MODULE_4__.EnvironmentService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.ChangeDetectorRef), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_router__WEBPACK_IMPORTED_MODULE_3__.Router));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: DynamicSectionComponent,
      selectors: [["theia-dynamic-section"]],
      decls: 9,
      vars: 8,
      consts: [[1, "row"], [1, "col-4", 3, "ngClass"], ["class", "collapse-button", 3, "click", 4, "ngIf"], [3, "actions", "actionSelected", 4, "ngIf"], [1, "col-8", 3, "ngClass"], [4, "ngIf", "ngIfElse"], ["showDescription", ""], [1, "collapse-button", 3, "click"], ["class", "bi bi-chevron-double-left", "fill", "currentColor", "height", "1em", "viewBox", "0 0 16 16", "width", "1em", "xmlns", "http://www.w3.org/2000/svg", 4, "ngIf"], ["class", "bi bi-chevron-double-right", "fill", "currentColor", "height", "1em", "viewBox", "0 0 16 16", "width", "1em", "xmlns", "http://www.w3.org/2000/svg", 4, "ngIf"], ["fill", "currentColor", "height", "1em", "viewBox", "0 0 16 16", "width", "1em", "xmlns", "http://www.w3.org/2000/svg", 1, "bi", "bi-chevron-double-left"], ["d", "M8.354 1.646a.5.5 0 0 1 0 .708L2.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z", "fill-rule", "evenodd"], ["d", "M12.354 1.646a.5.5 0 0 1 0 .708L6.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z", "fill-rule", "evenodd"], ["fill", "currentColor", "height", "1em", "viewBox", "0 0 16 16", "width", "1em", "xmlns", "http://www.w3.org/2000/svg", 1, "bi", "bi-chevron-double-right"], ["d", "M3.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L9.293 8 3.646 2.354a.5.5 0 0 1 0-.708z", "fill-rule", "evenodd"], ["d", "M7.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L13.293 8 7.646 2.354a.5.5 0 0 1 0-.708z", "fill-rule", "evenodd"], [3, "actions", "actionSelected"], [3, "actionId", "steps"], [1, "card"], [1, "card-body"], [3, "data", 4, "ngIf"], [3, "innerHTML", 4, "ngIf"], [3, "data"], [3, "innerHTML"]],
      template: function DynamicSectionComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "theia-layout")(1, "div", 0)(2, "div", 1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, DynamicSectionComponent_div_3_Template, 3, 2, "div", 2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, DynamicSectionComponent_theia_actions_4_Template, 1, 1, "theia-actions", 3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "div", 4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](6, DynamicSectionComponent_ng_container_6_Template, 2, 3, "ng-container", 5);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](7, DynamicSectionComponent_ng_template_7_Template, 4, 2, "ng-template", null, 6, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplateRefExtractor"]);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
        }
        if (rf & 2) {
          const _r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](8);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](6, _c1, ctx.collapsed));
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.currentAction);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !ctx.collapsed);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", ctx.collapsed ? "col-12" : "col-8");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.currentAction)("ngIfElse", _r3);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_5__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_5__.NgIf, ngx_markdown__WEBPACK_IMPORTED_MODULE_6__.MarkdownComponent, _actions_actions_component__WEBPACK_IMPORTED_MODULE_7__.ActionsComponent, _steps_steps_component__WEBPACK_IMPORTED_MODULE_8__.StepsComponent, _layout_layout_component__WEBPACK_IMPORTED_MODULE_9__.LayoutComponent],
      styles: [".collapse-button[_ngcontent-%COMP%] {\n  position: absolute;\n  top: -8px;\n  right: 8px;\n  z-index: 10;\n  width: 24px;\n  height: 24px;\n  cursor: pointer;\n  border: 1px solid #DFDFDF;\n  border-radius: 50%;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  font-size: 0.8rem;\n  background-color: white;\n}\n\n.collapsed[_ngcontent-%COMP%] {\n  flex-basis: 1px;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9keW5hbWljLXNlY3Rpb24vZHluYW1pYy1zZWN0aW9uLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0Usa0JBQUE7RUFDQSxTQUFBO0VBQ0EsVUFBQTtFQUNBLFdBQUE7RUFDQSxXQUFBO0VBQ0EsWUFBQTtFQUNBLGVBQUE7RUFDQSx5QkFBQTtFQUNBLGtCQUFBO0VBQ0EsYUFBQTtFQUNBLHVCQUFBO0VBQ0EsbUJBQUE7RUFDQSxpQkFBQTtFQUNBLHVCQUFBO0FBQ0Y7O0FBRUE7RUFDRSxlQUFBO0FBQ0YiLCJzb3VyY2VzQ29udGVudCI6WyIuY29sbGFwc2UtYnV0dG9uIHtcbiAgcG9zaXRpb246IGFic29sdXRlO1xuICB0b3A6IC04cHg7XG4gIHJpZ2h0OiA4cHg7XG4gIHotaW5kZXg6IDEwO1xuICB3aWR0aDogMjRweDtcbiAgaGVpZ2h0OiAyNHB4O1xuICBjdXJzb3I6IHBvaW50ZXI7XG4gIGJvcmRlcjogMXB4IHNvbGlkICNERkRGREY7XG4gIGJvcmRlci1yYWRpdXM6IDUwJTtcbiAgZGlzcGxheTogZmxleDtcbiAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIGZvbnQtc2l6ZTogMC44cmVtO1xuICBiYWNrZ3JvdW5kLWNvbG9yOiB3aGl0ZTtcbn1cblxuLmNvbGxhcHNlZCB7XG4gIGZsZXgtYmFzaXM6IDFweDtcbn1cbiJdLCJzb3VyY2VSb290IjoiIn0= */"]
    });
  }
  return DynamicSectionComponent;
})();

/***/ }),

/***/ 9426:
/*!*****************************************************!*\
  !*** ./src/app/components/error/error.component.ts ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ErrorComponent: () => (/* binding */ ErrorComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_window_ref_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../services/window-ref.service */ 6889);
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ 7947);



let ErrorComponent = /*#__PURE__*/(() => {
  class ErrorComponent {
    constructor(windowRef) {
      this.windowRef = windowRef;
      this.window = windowRef.nativeWindow;
    }
    reload() {
      this.window.location.reload();
    }
    static #_ = this.ɵfac = function ErrorComponent_Factory(t) {
      return new (t || ErrorComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_window_ref_service__WEBPACK_IMPORTED_MODULE_1__.WindowRefService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: ErrorComponent,
      selectors: [["theia-error"]],
      inputs: {
        header: "header",
        error: "error",
        description: "description"
      },
      decls: 21,
      vars: 3,
      consts: [[1, "container", "text-center", "mt-5"], [1, "row"], [1, "col"], ["alt", "RapidCloud", "src", "assets/img/logo.png"], [1, "row", "mt-5"], [1, "row", "mt-3"], ["routerLink", "/", 1, "btn", "btn-link"], ["href", "https://rapid-cloud.io/contact-us/", 1, "btn", "btn-link"]],
      template: function ErrorComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "main", 0)(1, "div", 1)(2, "div", 2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](3, "img", 3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "div", 4)(5, "div", 2)(6, "h1");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](8, "div", 5)(9, "div", 2)(10, "h2");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](11);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](12, "div", 5)(13, "div", 2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](14);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](15, "div", 4)(16, "div", 2)(17, "a", 6);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](18, "Home");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](19, "a", 7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](20, "Contact Support");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()()();
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](ctx.header);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](ctx.error);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", ctx.description, " ");
        }
      },
      dependencies: [_angular_router__WEBPACK_IMPORTED_MODULE_2__.RouterLink],
      styles: ["img[_ngcontent-%COMP%] {\n  height: 60px;\n  width: auto;\n  vertical-align: middle;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9lcnJvci9lcnJvci5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLFlBQUE7RUFDQSxXQUFBO0VBQ0Esc0JBQUE7QUFDRiIsInNvdXJjZXNDb250ZW50IjpbImltZyB7XG4gIGhlaWdodDogNjBweDtcbiAgd2lkdGg6IGF1dG87XG4gIHZlcnRpY2FsLWFsaWduOiBtaWRkbGU7XG59XG4iXSwic291cmNlUm9vdCI6IiJ9 */"]
    });
  }
  return ErrorComponent;
})();

/***/ }),

/***/ 7913:
/*!*******************************************************!*\
  !*** ./src/app/components/footer/footer.component.ts ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FooterComponent: () => (/* binding */ FooterComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_template_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../services/template.service */ 529);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var ngx_markdown__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ngx-markdown */ 1995);




function FooterComponent_div_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "markdown", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const column_r1 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", column_r1.class);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("data", column_r1.content);
  }
}
let FooterComponent = /*#__PURE__*/(() => {
  class FooterComponent {
    constructor(templateService) {
      this.templateService = templateService;
    }
    static #_ = this.ɵfac = function FooterComponent_Factory(t) {
      return new (t || FooterComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_template_service__WEBPACK_IMPORTED_MODULE_1__.TemplateService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: FooterComponent,
      selectors: [["theia-footer"]],
      decls: 3,
      vars: 3,
      consts: [[1, "footer", "d-flex", "justify-content-between", "px-5"], [3, "ngClass", 4, "ngFor", "ngForOf"], [3, "ngClass"], [3, "data"]],
      template: function FooterComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "footer", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, FooterComponent_div_1_Template, 2, 2, "div", 1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](2, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }
        if (rf & 2) {
          let tmp_0_0;
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", (tmp_0_0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](2, 1, ctx.templateService.template$)) == null ? null : tmp_0_0.footer == null ? null : tmp_0_0.footer.columns);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_2__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_2__.NgForOf, ngx_markdown__WEBPACK_IMPORTED_MODULE_3__.MarkdownComponent, _angular_common__WEBPACK_IMPORTED_MODULE_2__.AsyncPipe],
      styles: [".footer[_ngcontent-%COMP%] {\n  position: absolute;\n  bottom: 0;\n  width: 100%;\n  line-height: 5.5rem;\n  height: calc(5.5rem + 1px);\n  background-color: white;\n  border-top: 1px solid var(--gray-200, #EAECF0);\n}\n.footer[_ngcontent-%COMP%]     p {\n  margin-bottom: 0;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9mb290ZXIvZm9vdGVyLmNvbXBvbmVudC5zY3NzIiwid2VicGFjazovLy4vc3JjL19nbG9iYWxzLnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBRUE7RUFDRSxrQkFBQTtFQUNBLFNBQUE7RUFDQSxXQUFBO0VBQ0EsbUJDSmM7RURLZCwwQkFBQTtFQUNBLHVCQUFBO0VBQ0EsOENBQUE7QUFERjtBQUdFO0VBQ0UsZ0JBQUE7QUFESiIsInNvdXJjZXNDb250ZW50IjpbIkB1c2UgXCIuLi8uLi8uLi9nbG9iYWxzXCI7XG5cbi5mb290ZXIge1xuICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gIGJvdHRvbTogMDtcbiAgd2lkdGg6IDEwMCU7XG4gIGxpbmUtaGVpZ2h0OiBnbG9iYWxzLiRmb290ZXItaGVpZ2h0O1xuICBoZWlnaHQ6IGNhbGMoI3tnbG9iYWxzLiRmb290ZXItaGVpZ2h0fSArIDFweCk7XG4gIGJhY2tncm91bmQtY29sb3I6IHdoaXRlO1xuICBib3JkZXItdG9wOiAxcHggc29saWQgdmFyKC0tZ3JheS0yMDAsICNFQUVDRjApO1xuXG4gIDo6bmctZGVlcCBwIHtcbiAgICBtYXJnaW4tYm90dG9tOiAwO1xuICB9XG59XG4iLCIkZm9udC1mYW1pbHktYmFzZTogSW50ZXIsIHNhbnMtc2VyaWY7XG4kaGVhZGVyLWhlaWdodDogNC41cmVtO1xuJGZvb3Rlci1oZWlnaHQ6IDUuNXJlbTtcblxuJHByaW1hcnktMjAwOiAjOTZDMEUwO1xuJHByaW1hcnktNTAwOiAjMUI3NUJCO1xuJHByaW1hcnktNjAwOiAjMTk2QUFBO1xuJHByaW1hcnktNzAwOiAjMTM1Mzg1O1xuXG4kZ3JheS01MDogI0Y5RkFGQjtcbiRncmF5LTEwMDogI0YyRjRGNztcbiRncmF5LTIwMDogI0VBRUNGMDtcbiRncmF5LTMwMDogI0QwRDVERDtcbiRncmF5LTYwMDogIzQ3NTQ2NztcbiRncmF5LTcwMDogIzM0NDA1NDtcbiRncmF5LTgwMDogIzFEMjkzOTtcbiRncmF5LTkwMDogIzEwMTgyODtcblxuXG4kbGluay1jb2xvcjogJHByaW1hcnktNTAwICFkZWZhdWx0O1xuXG5AbWl4aW4gaGlkZS1zY3JvbGxiYXJzIHtcbiAgc2Nyb2xsYmFyLXdpZHRoOiBub25lO1xuICAtbXMtb3ZlcmZsb3ctc3R5bGU6IG5vbmU7XG4gICY6Oi13ZWJraXQtc2Nyb2xsYmFyIHtcbiAgICBkaXNwbGF5OiBub25lO1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9 */"]
    });
  }
  return FooterComponent;
})();

/***/ }),

/***/ 3150:
/*!***************************************************!*\
  !*** ./src/app/components/grid/grid.component.ts ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   GridComponent: () => (/* binding */ GridComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/forms */ 8849);
/* harmony import */ var src_app_models_grid__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! src/app/models/grid */ 1708);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _pagination_pagination_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../pagination/pagination.component */ 2649);






function GridComponent_ng_container_0_div_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 3)(1, "div", 4)(2, "span", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](3, "Loading...");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
  }
}
function GridComponent_ng_container_0_ng_container_2_Template(rf, ctx) {
  if (rf & 1) {
    const _r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "theia-pagination", 6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("pageChange", function GridComponent_ng_container_0_ng_container_2_Template_theia_pagination_pageChange_1_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r6);
      const ctx_r5 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r5.onPageChange($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("totalItems", ctx_r2.paginationData.size)("itemsPerPage", ctx_r2.paginationData.limit);
  }
}
function GridComponent_ng_container_0_ng_template_3_th_4_div_4__svg_svg_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "svg", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "path", 21);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
function GridComponent_ng_container_0_ng_template_3_th_4_div_4__svg_svg_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "svg", 22);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "path", 23);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
function GridComponent_ng_container_0_ng_template_3_th_4_div_4__svg_svg_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "svg", 24);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "path", 25);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
function GridComponent_ng_container_0_ng_template_3_th_4_div_4__svg_svg_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "svg", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "path", 27);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
function GridComponent_ng_container_0_ng_template_3_th_4_div_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 15);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, GridComponent_ng_container_0_ng_template_3_th_4_div_4__svg_svg_1_Template, 2, 0, "svg", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, GridComponent_ng_container_0_ng_template_3_th_4_div_4__svg_svg_2_Template, 2, 0, "svg", 17);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, GridComponent_ng_container_0_ng_template_3_th_4_div_4__svg_svg_3_Template, 2, 0, "svg", 18);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, GridComponent_ng_container_0_ng_template_3_th_4_div_4__svg_svg_4_Template, 2, 0, "svg", 19);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const column_r11 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    const ctx_r12 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r12.sortKey !== column_r11 || ctx_r12.sortOrder !== ctx_r12.SortOrder.Asc);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r12.sortKey === column_r11 && ctx_r12.sortOrder === ctx_r12.SortOrder.Asc);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r12.sortKey !== column_r11 || ctx_r12.sortOrder !== ctx_r12.SortOrder.Desc);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r12.sortKey === column_r11 && ctx_r12.sortOrder === ctx_r12.SortOrder.Desc);
  }
}
function GridComponent_ng_container_0_ng_template_3_th_4_Template(rf, ctx) {
  if (rf & 1) {
    const _r19 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "th", 12);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function GridComponent_ng_container_0_ng_template_3_th_4_Template_th_click_0_listener() {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r19);
      const column_r11 = restoredCtx.$implicit;
      const ctx_r18 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r18.sortBy(column_r11));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 13)(2, "span");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, GridComponent_ng_container_0_ng_template_3_th_4_div_4_Template, 5, 4, "div", 14);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const column_r11 = ctx.$implicit;
    const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](column_r11);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !ctx_r7.step.pagination);
  }
}
function GridComponent_ng_container_0_ng_template_3_ng_container_6_tr_1_td_1_a_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "a", 33);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const value_r23 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("href", value_r23, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsanitizeUrl"]);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](value_r23);
  }
}
function GridComponent_ng_container_0_ng_template_3_ng_container_6_tr_1_td_1_ng_template_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](0);
  }
  if (rf & 2) {
    const value_r23 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", value_r23, " ");
  }
}
function GridComponent_ng_container_0_ng_template_3_ng_container_6_tr_1_td_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "td");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, GridComponent_ng_container_0_ng_template_3_ng_container_6_tr_1_td_1_a_1_Template, 2, 2, "a", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, GridComponent_ng_container_0_ng_template_3_ng_container_6_tr_1_td_1_ng_template_2_Template, 1, 1, "ng-template", null, 32, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplateRefExtractor"]);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const value_r23 = ctx.$implicit;
    const _r25 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](3);
    const ctx_r22 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r22.isLink(value_r23))("ngIfElse", _r25);
  }
}
const _c0 = function (a0, a1) {
  return {
    "table-primary": a0,
    link: a1
  };
};
function GridComponent_ng_container_0_ng_template_3_ng_container_6_tr_1_Template(rf, ctx) {
  if (rf & 1) {
    const _r30 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "tr", 29);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function GridComponent_ng_container_0_ng_template_3_ng_container_6_tr_1_Template_tr_click_0_listener() {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r30);
      const row_r21 = restoredCtx.$implicit;
      const ctx_r29 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r29.onRowSelected(row_r21));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, GridComponent_ng_container_0_ng_template_3_ng_container_6_tr_1_td_1_Template, 4, 2, "td", 30);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const row_r21 = ctx.$implicit;
    const ctx_r20 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction2"](2, _c0, ctx_r20.selectedRowId === row_r21.id, !ctx_r20.step.readonly));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r20.getValues(row_r21));
  }
}
function GridComponent_ng_container_0_ng_template_3_ng_container_6_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, GridComponent_ng_container_0_ng_template_3_ng_container_6_tr_1_Template, 2, 5, "tr", 28);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r8 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r8.data);
  }
}
function GridComponent_ng_container_0_ng_template_3_ng_template_7_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "tr", 34)(1, "td", 35);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2, " No results found ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r10 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("colSpan", ctx_r10.columns.length);
  }
}
function GridComponent_ng_container_0_ng_template_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 7)(1, "table", 8)(2, "thead")(3, "tr");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, GridComponent_ng_container_0_ng_template_3_th_4_Template, 5, 2, "th", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "tbody");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](6, GridComponent_ng_container_0_ng_template_3_ng_container_6_Template, 2, 1, "ng-container", 10);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](7, GridComponent_ng_container_0_ng_template_3_ng_template_7_Template, 3, 1, "ng-template", null, 11, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplateRefExtractor"]);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
  }
  if (rf & 2) {
    const _r9 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](8);
    const ctx_r4 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r4.columns);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r4.data.length)("ngIfElse", _r9);
  }
}
function GridComponent_ng_container_0_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, GridComponent_ng_container_0_div_1_Template, 4, 0, "div", 1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, GridComponent_ng_container_0_ng_container_2_Template, 2, 2, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, GridComponent_ng_container_0_ng_template_3_Template, 9, 3, "ng-template", null, 2, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplateRefExtractor"]);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const _r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](4);
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r0.loading)("ngIfElse", _r3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r0.step.pagination && ctx_r0.paginationData);
  }
}
let GridComponent = /*#__PURE__*/(() => {
  class GridComponent {
    constructor() {
      this.formGroup = new _angular_forms__WEBPACK_IMPORTED_MODULE_1__.UntypedFormGroup({});
      this.data = [];
      this.loading = false;
      this.sortKey = '';
      this.sortOrder = src_app_models_grid__WEBPACK_IMPORTED_MODULE_2__.SortOrder.Asc;
      this.selectedRowId = '';
      this.selected = new _angular_core__WEBPACK_IMPORTED_MODULE_0__.EventEmitter();
      this.sort = new _angular_core__WEBPACK_IMPORTED_MODULE_0__.EventEmitter();
      this.pageChange = new _angular_core__WEBPACK_IMPORTED_MODULE_0__.EventEmitter();
      this.SortOrder = src_app_models_grid__WEBPACK_IMPORTED_MODULE_2__.SortOrder;
    }
    get columns() {
      return this.step?.columns || [];
    }
    ngOnInit() {
      this.formGroup.reset();
    }
    getHeaders(row) {
      return Object.keys(row);
    }
    getValues(row) {
      return this.columns.map(column => row[column]);
    }
    sortBy(column) {
      this.sort.emit(column);
    }
    onPageChange(page) {
      this.pageChange.emit(page);
    }
    onRowSelected(row) {
      this.selected.emit({
        isNew: false,
        data: row
      });
    }
    isLink(value) {
      return /^https?:\/\/[^ ]+$/.test(value);
    }
    static #_ = this.ɵfac = function GridComponent_Factory(t) {
      return new (t || GridComponent)();
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: GridComponent,
      selectors: [["theia-grid"]],
      inputs: {
        step: "step",
        formGroup: "formGroup",
        data: "data",
        loading: "loading",
        paginationData: "paginationData",
        sortKey: "sortKey",
        sortOrder: "sortOrder",
        selectedRowId: "selectedRowId"
      },
      outputs: {
        selected: "selected",
        sort: "sort",
        pageChange: "pageChange"
      },
      decls: 1,
      vars: 1,
      consts: [[4, "ngIf"], ["class", "d-flex justify-content-center loader", 4, "ngIf", "ngIfElse"], ["loaded", ""], [1, "d-flex", "justify-content-center", "loader"], ["role", "status", 1, "spinner-border", "spinner-big", "m-4", "text-primary"], [1, "visually-hidden"], [3, "totalItems", "itemsPerPage", "pageChange"], [1, ""], [1, "table", "table-hover", "table-sm", "table-bordered", "text-nowrap"], [3, "click", 4, "ngFor", "ngForOf"], [4, "ngIf", "ngIfElse"], ["noResults", ""], [3, "click"], [1, "header"], ["class", "sort-caret", 4, "ngIf"], [1, "sort-caret"], ["class", "bi bi-caret-up", "fill", "currentColor", "height", "1em", "viewBox", "0 0 16 16", "width", "1em", "xmlns", "http://www.w3.org/2000/svg", 4, "ngIf"], ["class", "bi bi-caret-up-fill", "fill", "currentColor", "height", "1em", "viewBox", "0 0 16 16", "width", "1em", "xmlns", "http://www.w3.org/2000/svg", 4, "ngIf"], ["class", "bi bi-caret-down", "fill", "currentColor", "height", "1em", "viewBox", "0 0 16 16", "width", "1em", "xmlns", "http://www.w3.org/2000/svg", 4, "ngIf"], ["class", "bi bi-caret-down-fill", "fill", "currentColor", "height", "1em", "viewBox", "0 0 16 16", "width", "1em", "xmlns", "http://www.w3.org/2000/svg", 4, "ngIf"], ["fill", "currentColor", "height", "1em", "viewBox", "0 0 16 16", "width", "1em", "xmlns", "http://www.w3.org/2000/svg", 1, "bi", "bi-caret-up"], ["d", "M3.204 11L8 5.519 12.796 11H3.204zm-.753-.659l4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659z", "fill-rule", "evenodd"], ["fill", "currentColor", "height", "1em", "viewBox", "0 0 16 16", "width", "1em", "xmlns", "http://www.w3.org/2000/svg", 1, "bi", "bi-caret-up-fill"], ["d", "M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"], ["fill", "currentColor", "height", "1em", "viewBox", "0 0 16 16", "width", "1em", "xmlns", "http://www.w3.org/2000/svg", 1, "bi", "bi-caret-down"], ["d", "M3.204 5L8 10.481 12.796 5H3.204zm-.753.659l4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659z", "fill-rule", "evenodd"], ["fill", "currentColor", "height", "1em", "viewBox", "0 0 16 16", "width", "1em", "xmlns", "http://www.w3.org/2000/svg", 1, "bi", "bi-caret-down-fill"], ["d", "M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"], [3, "ngClass", "click", 4, "ngFor", "ngForOf"], [3, "ngClass", "click"], [4, "ngFor", "ngForOf"], [3, "href", 4, "ngIf", "ngIfElse"], ["notLink", ""], [3, "href"], [1, "text-center"], [3, "colSpan"]],
      template: function GridComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](0, GridComponent_ng_container_0_Template, 5, 3, "ng-container", 0);
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.step);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_3__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_3__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_3__.NgIf, _pagination_pagination_component__WEBPACK_IMPORTED_MODULE_4__.PaginationComponent],
      styles: ["[_nghost-%COMP%] {\n  border-radius: 12px;\n  border: 1px solid #EAECF0;\n  box-shadow: 0 1px 2px 0 rgba(16, 24, 40, 0.06), 0 1px 3px 0 rgba(16, 24, 40, 0.1);\n  padding: 0;\n  display: block;\n  overflow: auto;\n}\n\ntr.link[_ngcontent-%COMP%] {\n  cursor: pointer;\n}\n\ndiv.sort-caret[_ngcontent-%COMP%] {\n  display: flex;\n  flex-direction: column;\n  font-size: 0.8rem;\n}\ndiv.sort-caret[_ngcontent-%COMP%]   svg[_ngcontent-%COMP%]:first-child {\n  margin-bottom: -3px;\n}\n\ndiv.header[_ngcontent-%COMP%] {\n  display: flex;\n  justify-content: space-between;\n  cursor: pointer;\n}\n\ntable[_ngcontent-%COMP%] {\n  border-top-left-radius: 12px;\n  border-top-right-radius: 12px;\n  border: 1px solid #EAECF0;\n  border-collapse: collapse;\n  overflow: hidden;\n  box-shadow: 0 0 0 1px #EAECF0;\n}\ntable[_ngcontent-%COMP%]   thead[_ngcontent-%COMP%]   th[_ngcontent-%COMP%] {\n  padding: 0.75rem 1.5rem;\n  background-color: #F9FAFB;\n}\ntable[_ngcontent-%COMP%]   tbody[_ngcontent-%COMP%]   tr[_ngcontent-%COMP%]:nth-child(even) {\n  background-color: #F9FAFB;\n}\ntable[_ngcontent-%COMP%]   tbody[_ngcontent-%COMP%]   td[_ngcontent-%COMP%] {\n  padding: 1rem 1.5rem;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9ncmlkL2dyaWQuY29tcG9uZW50LnNjc3MiLCJ3ZWJwYWNrOi8vLi9zcmMvX2dsb2JhbHMuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFFQTtFQUNFLG1CQUFBO0VBQ0EseUJBQUE7RUFDQSxpRkFBQTtFQUNBLFVBQUE7RUFDQSxjQUFBO0VBQ0EsY0FBQTtBQURGOztBQUlBO0VBQ0UsZUFBQTtBQURGOztBQUlBO0VBS0UsYUFBQTtFQUNBLHNCQUFBO0VBQ0EsaUJBQUE7QUFMRjtBQURFO0VBQ0UsbUJBQUE7QUFHSjs7QUFLQTtFQUNFLGFBQUE7RUFDQSw4QkFBQTtFQUNBLGVBQUE7QUFGRjs7QUFVQTtFQUNFLDRCQUFBO0VBQ0EsNkJBQUE7RUFDQSx5QkFBQTtFQUNBLHlCQUFBO0VBQ0EsZ0JBQUE7RUFDQSw2QkFBQTtBQVBGO0FBVUk7RUFDRSx1QkFBQTtFQUNBLHlCQ3RDSTtBRDhCVjtBQVlJO0VBQ0UseUJDM0NJO0FEaUNWO0FBWUk7RUFDRSxvQkFBQTtBQVZOIiwic291cmNlc0NvbnRlbnQiOlsiQHVzZSBcIi4uLy4uLy4uL2dsb2JhbHNcIjtcblxuOmhvc3Qge1xuICBib3JkZXItcmFkaXVzOiAxMnB4O1xuICBib3JkZXI6IDFweCBzb2xpZCBnbG9iYWxzLiRncmF5LTIwMDtcbiAgYm94LXNoYWRvdzogMCAxcHggMnB4IDAgcmdiYSgxNiwgMjQsIDQwLCAwLjA2KSwgMCAxcHggM3B4IDAgcmdiYSgxNiwgMjQsIDQwLCAwLjEwKTtcbiAgcGFkZGluZzogMDtcbiAgZGlzcGxheTogYmxvY2s7XG4gIG92ZXJmbG93OiBhdXRvO1xufVxuXG50ci5saW5rIHtcbiAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG5kaXYuc29ydC1jYXJldCB7XG4gICYgc3ZnOmZpcnN0LWNoaWxkIHtcbiAgICBtYXJnaW4tYm90dG9tOiAtM3B4O1xuICB9XG5cbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjtcbiAgZm9udC1zaXplOiAwLjhyZW07XG59XG5cbmRpdi5oZWFkZXIge1xuICBkaXNwbGF5OiBmbGV4O1xuICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWJldHdlZW47XG4gIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuZGl2LmdyaWQtdGFibGUge1xuICAvL21heC1oZWlnaHQ6IGNhbGMoMTAwdmggLSAxNXJlbSk7XG4gIC8vb3ZlcmZsb3c6IGF1dG87XG59XG5cbnRhYmxlIHtcbiAgYm9yZGVyLXRvcC1sZWZ0LXJhZGl1czogMTJweDtcbiAgYm9yZGVyLXRvcC1yaWdodC1yYWRpdXM6IDEycHg7XG4gIGJvcmRlcjogMXB4IHNvbGlkIGdsb2JhbHMuJGdyYXktMjAwO1xuICBib3JkZXItY29sbGFwc2U6IGNvbGxhcHNlO1xuICBvdmVyZmxvdzogaGlkZGVuO1xuICBib3gtc2hhZG93OjAgMCAwIDFweCBnbG9iYWxzLiRncmF5LTIwMDtcblxuICB0aGVhZCB7XG4gICAgdGgge1xuICAgICAgcGFkZGluZzogLjc1cmVtIDEuNXJlbTtcbiAgICAgIGJhY2tncm91bmQtY29sb3I6IGdsb2JhbHMuJGdyYXktNTA7XG4gICAgfVxuICB9XG4gIHRib2R5IHtcbiAgICB0cjpudGgtY2hpbGQoZXZlbikge1xuICAgICAgYmFja2dyb3VuZC1jb2xvcjogZ2xvYmFscy4kZ3JheS01MDtcbiAgICB9XG4gICAgdGQge1xuICAgICAgcGFkZGluZzogMXJlbSAxLjVyZW07XG4gICAgfVxuICB9XG59XG4iLCIkZm9udC1mYW1pbHktYmFzZTogSW50ZXIsIHNhbnMtc2VyaWY7XG4kaGVhZGVyLWhlaWdodDogNC41cmVtO1xuJGZvb3Rlci1oZWlnaHQ6IDUuNXJlbTtcblxuJHByaW1hcnktMjAwOiAjOTZDMEUwO1xuJHByaW1hcnktNTAwOiAjMUI3NUJCO1xuJHByaW1hcnktNjAwOiAjMTk2QUFBO1xuJHByaW1hcnktNzAwOiAjMTM1Mzg1O1xuXG4kZ3JheS01MDogI0Y5RkFGQjtcbiRncmF5LTEwMDogI0YyRjRGNztcbiRncmF5LTIwMDogI0VBRUNGMDtcbiRncmF5LTMwMDogI0QwRDVERDtcbiRncmF5LTYwMDogIzQ3NTQ2NztcbiRncmF5LTcwMDogIzM0NDA1NDtcbiRncmF5LTgwMDogIzFEMjkzOTtcbiRncmF5LTkwMDogIzEwMTgyODtcblxuXG4kbGluay1jb2xvcjogJHByaW1hcnktNTAwICFkZWZhdWx0O1xuXG5AbWl4aW4gaGlkZS1zY3JvbGxiYXJzIHtcbiAgc2Nyb2xsYmFyLXdpZHRoOiBub25lO1xuICAtbXMtb3ZlcmZsb3ctc3R5bGU6IG5vbmU7XG4gICY6Oi13ZWJraXQtc2Nyb2xsYmFyIHtcbiAgICBkaXNwbGF5OiBub25lO1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9 */"]
    });
  }
  return GridComponent;
})();

/***/ }),

/***/ 6471:
/*!*******************************************************!*\
  !*** ./src/app/components/header/header.component.ts ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   HeaderComponent: () => (/* binding */ HeaderComponent)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ 8071);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ 7474);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_environment_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../services/environment.service */ 1574);
/* harmony import */ var _services_cloud_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/cloud.service */ 9509);
/* harmony import */ var _services_allowed_apps_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/allowed-apps.service */ 9726);
/* harmony import */ var _auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @auth0/auth0-angular */ 6742);
/* harmony import */ var _services_window_ref_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../services/window-ref.service */ 6889);
/* harmony import */ var _services_logout_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../services/logout.service */ 6751);
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/router */ 7947);
/* harmony import */ var _directives_dropdown_directive__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../directives/dropdown.directive */ 1501);
/* harmony import */ var _directives_submenu_directive__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../directives/submenu.directive */ 8520);














function HeaderComponent_div_8_ng_container_4_Template(rf, ctx) {
  if (rf & 1) {
    const _r9 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 17);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function HeaderComponent_div_8_ng_container_4_Template_div_click_1_listener($event) {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r9);
      const app_r7 = restoredCtx.$implicit;
      const ctx_r8 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r8.selectApp($event, app_r7.id));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "div", 18)(3, "span");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "span");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const app_r7 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](app_r7.title);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](app_r7.description);
  }
}
function HeaderComponent_div_8_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 13)(1, "div", 14);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2, "AWS");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "div", 15);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, HeaderComponent_div_8_ng_container_4_Template, 7, 2, "ng-container", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](5, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](5, 1, ctx_r0.allowedAWSApps$));
  }
}
function HeaderComponent_div_10_ng_container_4_Template(rf, ctx) {
  if (rf & 1) {
    const _r13 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 17);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function HeaderComponent_div_10_ng_container_4_Template_div_click_1_listener($event) {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r13);
      const app_r11 = restoredCtx.$implicit;
      const ctx_r12 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r12.selectApp($event, app_r11.id));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "div", 18)(3, "span");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "span");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const app_r11 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](app_r11.title);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](app_r11.description);
  }
}
function HeaderComponent_div_10_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 13)(1, "div", 14);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2, "Azure");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "div", 15);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, HeaderComponent_div_10_ng_container_4_Template, 7, 2, "ng-container", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](5, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](5, 1, ctx_r1.allowedAzureApps$));
  }
}
function HeaderComponent_div_12_ng_container_4_Template(rf, ctx) {
  if (rf & 1) {
    const _r17 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 17);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function HeaderComponent_div_12_ng_container_4_Template_div_click_1_listener($event) {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r17);
      const app_r15 = restoredCtx.$implicit;
      const ctx_r16 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r16.selectApp($event, app_r15.id));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "div", 18)(3, "span");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "span");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const app_r15 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](app_r15.title);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](app_r15.description);
  }
}
function HeaderComponent_div_12_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 13)(1, "div", 14);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2, "GCP");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "div", 15);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, HeaderComponent_div_12_ng_container_4_Template, 7, 2, "ng-container", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](5, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](5, 1, ctx_r2.allowedGCPApps$));
  }
}
function HeaderComponent_ng_container_22_ng_container_21_li_1_Template(rf, ctx) {
  if (rf & 1) {
    const _r24 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "li")(1, "a", 22);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function HeaderComponent_ng_container_22_ng_container_21_li_1_Template_a_click_1_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r24);
      const env_r20 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
      const ctx_r22 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r22.selectEnv($event, env_r20));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const env_r20 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](env_r20.name);
  }
}
function HeaderComponent_ng_container_22_ng_container_21_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, HeaderComponent_ng_container_22_ng_container_21_li_1_Template, 3, 1, "li", 11);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](2, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const env_r20 = ctx.$implicit;
    const ctx_r19 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    let tmp_0_0;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", env_r20.name !== ((tmp_0_0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](2, 1, ctx_r19.currentEnv$)) == null ? null : tmp_0_0.name));
  }
}
function HeaderComponent_ng_container_22_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "li")(2, "div", 19)(3, "span")(4, "strong");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](5, "Account:");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](7, "span")(8, "strong");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](9, "Region:");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](10);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](11, "span")(12, "strong");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](13, "VPC:");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](14);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](15, "li");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](16, "hr", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](17, "li")(18, "span", 21)(19, "strong");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](20, "Recent environments");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](21, HeaderComponent_ng_container_22_ng_container_21_Template, 3, 3, "ng-container", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](22, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](23, "li");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](24, "hr", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const currentEnv_r18 = ctx.ngIf;
    const ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", currentEnv_r18.account, "");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", currentEnv_r18.region, "");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", currentEnv_r18.vpc, "");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](22, 4, ctx_r3.recentEnvironments$));
  }
}
function HeaderComponent_li_24_li_4_li_4_Template(rf, ctx) {
  if (rf & 1) {
    const _r32 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "li")(1, "a", 22);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function HeaderComponent_li_24_li_4_li_4_Template_a_click_1_listener($event) {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r32);
      const env_r30 = restoredCtx.$implicit;
      const ctx_r31 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r31.selectEnv($event, env_r30.env));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const env_r30 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](env_r30.name);
  }
}
function HeaderComponent_li_24_li_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "li", 23)(1, "span", 24);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "ul", 25);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, HeaderComponent_li_24_li_4_li_4_Template, 3, 1, "li", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const workload_r28 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](workload_r28.name);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", workload_r28.children);
  }
}
function HeaderComponent_li_24_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "li", 23)(1, "span", 24);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "ul", 25);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, HeaderComponent_li_24_li_4_Template, 5, 2, "li", 12);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const client_r26 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](client_r26.name);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", client_r26.children);
  }
}
const _c0 = function () {
  return ["/action/setup/activate"];
};
const _c1 = function () {
  return ["/action/setup/users"];
};
const _c2 = function () {
  return ["/action/setup/access_create_role"];
};
const _c3 = function () {
  return ["/action/setup/environments"];
};
function HeaderComponent_ng_container_26_Template(rf, ctx) {
  if (rf & 1) {
    const _r35 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "li", 3)(2, "a", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](3, "img", 27);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "ul", 10)(5, "li")(6, "div", 28);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](7, "img", 27);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](8, "div")(9, "span", 29);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](10);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](11, "span", 29);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](12);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](13, "li");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](14, "hr", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](15, "li")(16, "a", 30);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](17, "svg", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](18, "path", 32);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](19, " Profile");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceHTML"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](20, "li")(21, "a", 30);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](22, "svg", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](23, "path", 33);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](24, " Users");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceHTML"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](25, "li")(26, "a", 30);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](27, "svg", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](28, "path", 33);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](29, " Roles");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceHTML"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](30, "li")(31, "a", 30);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](32, "svg", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](33, "path", 34);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](34, " Environments");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceHTML"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](35, "li");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](36, "hr", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](37, "li")(38, "a", 35);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](39, "svg", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](40, "path", 36);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](41, " Contact Us");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceHTML"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](42, "li");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](43, "hr", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](44, "li")(45, "a", 22);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function HeaderComponent_ng_container_26_Template_a_click_45_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r35);
      const ctx_r34 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r34.logout($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](46, "svg", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](47, "path", 37);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](48, " Logout");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const user_r33 = ctx.ngIf;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngSrc", user_r33.picture);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngSrc", user_r33.picture);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](user_r33.nickname);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](user_r33.email);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("routerLink", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction0"](8, _c0));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("routerLink", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction0"](9, _c1));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("routerLink", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction0"](10, _c2));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("routerLink", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction0"](11, _c3));
  }
}
let HeaderComponent = /*#__PURE__*/(() => {
  class HeaderComponent {
    get selectedCloud() {
      return this.availableClouds$.value[this.selectedCloud$.value];
    }
    get selectedApp() {
      return this.allowedApps$.value[this.selectedApp$.value];
    }
    constructor(environmentService, cloudService, allowedAppsService, authService, windowRef, logoutService, baseHref) {
      this.environmentService = environmentService;
      this.cloudService = cloudService;
      this.allowedAppsService = allowedAppsService;
      this.authService = authService;
      this.windowRef = windowRef;
      this.logoutService = logoutService;
      this.baseHref = baseHref;
      this.collapsed = true;
      this.allowedAWSApps$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject([]);
      this.allowedAzureApps$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject([]);
      this.allowedGCPApps$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject([]);
      this.recentEnvironments$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject(undefined);
      this.currentEnv$ = environmentService.getCurrentEnvironment();
      this.selectedCloud$ = cloudService.getSelectedCloud();
      this.selectedApp$ = allowedAppsService.getSelectedApp();
      this.recentEnvironments$ = environmentService.getRecentEnvironments();
      this.environments$ = environmentService.environments$;
      this.environmentsTree$ = environmentService.environmentsTree$;
      this.user$ = authService.user$;
      this.window = windowRef.nativeWindow;
      this.availableClouds$ = cloudService.availableClouds$;
      this.allowedApps$ = allowedAppsService.allowedApps$;
    }
    ngOnInit() {
      this.allowedAWSApps$.next(this.getAllowedAppsForCloud('aws'));
      this.allowedAzureApps$.next(this.getAllowedAppsForCloud('azure'));
      this.allowedGCPApps$.next(this.getAllowedAppsForCloud('gcp'));
    }
    toggle() {
      this.collapsed = !this.collapsed;
    }
    selectEnv(event, env) {
      if (!env) {
        return;
      }
      event.preventDefault();
      this.environmentService.setCurrentEnvironment(env);
    }
    selectCloud(cloud) {
      if (!cloud) {
        return;
      }
      this.cloudService.setSelectedCloud(cloud);
    }
    selectApp(event, app) {
      if (!app) {
        return;
      }
      event.preventDefault();
      this.allowedAppsService.setSelectedApp(app);
      this.selectCloud(this.allowedApps$.value[app].cloud);
    }
    getEntries(obj) {
      if (!obj) {
        return [];
      }
      return Object.entries(obj).map(e => ({
        key: e[0],
        value: e[1]
      }));
    }
    getEnvFromValue(value) {
      return value;
    }
    getAllowedAppsForCloud(cloud) {
      return Object.entries(this.allowedApps$.value).reduce((previousValue, [currentKey, currentValue]) => {
        if (currentValue.cloud === cloud) {
          previousValue.push({
            id: currentKey,
            ...currentValue
          });
        }
        return previousValue;
      }, []);
    }
    logout(e) {
      e.preventDefault();
      this.logoutService.logout().pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_2__.finalize)(() => {
        this.authService.logout({
          logoutParams: {
            returnTo: this.window.location.origin + this.baseHref.replace(/\/$/, '')
          }
        });
      })).subscribe();
    }
    static #_ = this.ɵfac = function HeaderComponent_Factory(t) {
      return new (t || HeaderComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_environment_service__WEBPACK_IMPORTED_MODULE_3__.EnvironmentService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_cloud_service__WEBPACK_IMPORTED_MODULE_4__.CloudService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_allowed_apps_service__WEBPACK_IMPORTED_MODULE_5__.AllowedAppsService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_auth0_auth0_angular__WEBPACK_IMPORTED_MODULE_6__.AuthService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_window_ref_service__WEBPACK_IMPORTED_MODULE_7__.WindowRefService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_logout_service__WEBPACK_IMPORTED_MODULE_8__.LogoutService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_common__WEBPACK_IMPORTED_MODULE_9__.APP_BASE_HREF));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: HeaderComponent,
      selectors: [["theia-header"]],
      decls: 28,
      vars: 22,
      consts: [[1, "navbar", "navbar-expand-lg", "navbar-light", "border-bottom"], [1, "container-fluid"], [1, "navbar-nav", "w-100", "align-items-center"], [1, "nav-item", "dropdown"], ["href", "", "role", "button", "theiaDropdown", "", 1, "nav-link", "dropdown-toggle"], [1, "application"], [1, "application-menu-new"], ["class", "section", 4, "ngIf"], [1, "nav-item", "dropdown", "flex-grow-1"], [1, "blue", "me-1"], [1, "dropdown-menu"], [4, "ngIf"], ["theiaSubmenu", "", 4, "ngFor", "ngForOf"], [1, "section"], [1, "header"], [1, "navigation"], [4, "ngFor", "ngForOf"], [1, "nav-item", 3, "click"], [1, "description"], [1, "d-flex", "flex-column", "text-nowrap", "gap-2", "env-info", "mb-1"], [1, "dropdown-divider"], [1, "dropdown-item-text"], ["href", "", 1, "dropdown-item", 3, "click"], ["theiaSubmenu", ""], [1, "dropdown-item"], [1, "dropdown-menu", "submenu"], ["href", "", "role", "button", "theiaDropdown", "", 1, "nav-link"], ["alt", "", "height", "40", "width", "40", 1, "user-picture", 3, "ngSrc"], [1, "user-info"], [1, "text-nowrap"], ["href", "", 1, "dropdown-item", 3, "routerLink"], ["xmlns", "http://www.w3.org/2000/svg", "width", "16", "height", "16", "viewBox", "0 0 16 16", "fill", "none"], ["d", "M13.3334 14C13.3334 13.0696 13.3334 12.6044 13.2185 12.2259C12.96 11.3736 12.293 10.7067 11.4408 10.4482C11.0623 10.3333 10.5971 10.3333 9.66668 10.3333H6.33336C5.40298 10.3333 4.93779 10.3333 4.55926 10.4482C3.70699 10.7067 3.04005 11.3736 2.78151 12.2259C2.66669 12.6044 2.66669 13.0696 2.66669 14M11 5C11 6.65685 9.65687 8 8.00002 8C6.34317 8 5.00002 6.65685 5.00002 5C5.00002 3.34315 6.34317 2 8.00002 2C9.65687 2 11 3.34315 11 5Z", "stroke", "#344054", "stroke-width", "1.5", "stroke-linecap", "round", "stroke-linejoin", "round"], ["d", "M14.6666 14V12.6667C14.6666 11.4241 13.8168 10.38 12.6666 10.084M10.3333 2.19384C11.3106 2.58943 12 3.54754 12 4.66667C12 5.78579 11.3106 6.7439 10.3333 7.13949M11.3333 14C11.3333 12.7575 11.3333 12.1362 11.1303 11.6462C10.8597 10.9928 10.3405 10.4736 9.68714 10.203C9.19708 10 8.57582 10 7.33331 10H5.33331C4.0908 10 3.46955 10 2.97949 10.203C2.32608 10.4736 1.80695 10.9928 1.5363 11.6462C1.33331 12.1362 1.33331 12.7575 1.33331 14M8.99998 4.66667C8.99998 6.13943 7.80607 7.33333 6.33331 7.33333C4.86055 7.33333 3.66665 6.13943 3.66665 4.66667C3.66665 3.19391 4.86055 2 6.33331 2C7.80607 2 8.99998 3.19391 8.99998 4.66667Z", "stroke", "#344054", "stroke-width", "1.5", "stroke-linecap", "round", "stroke-linejoin", "round"], ["d", "M5.33333 11.3333H10.6667M7.34513 1.84267L2.82359 5.35942C2.52135 5.5945 2.37022 5.71204 2.26135 5.85924C2.16491 5.98963 2.09307 6.13652 2.04935 6.2927C2 6.46901 2 6.66046 2 7.04337V11.8667C2 12.6134 2 12.9868 2.14532 13.272C2.27316 13.5229 2.47713 13.7268 2.72801 13.8547C3.01323 14 3.3866 14 4.13333 14H11.8667C12.6134 14 12.9868 14 13.272 13.8547C13.5229 13.7268 13.7268 13.5229 13.8547 13.272C14 12.9868 14 12.6134 14 11.8667V7.04337C14 6.66046 14 6.46901 13.9506 6.2927C13.9069 6.13652 13.8351 5.98963 13.7386 5.85924C13.6298 5.71204 13.4787 5.5945 13.1764 5.35942L8.65487 1.84267C8.42065 1.6605 8.30354 1.56941 8.17423 1.5344C8.06013 1.50351 7.93987 1.50351 7.82577 1.5344C7.69646 1.56941 7.57935 1.6605 7.34513 1.84267Z", "stroke", "#344054", "stroke-width", "1.5", "stroke-linecap", "round", "stroke-linejoin", "round"], ["href", "https://rapid-cloud.io/contact-us/", 1, "dropdown-item"], ["d", "M14.3333 11.9998L9.90474 7.99984M6.09522 7.99984L1.66667 11.9998M1.33331 4.6665L6.77659 8.4768C7.21737 8.78535 7.43776 8.93962 7.67749 8.99938C7.88924 9.05216 8.11072 9.05216 8.32247 8.99938C8.5622 8.93962 8.78259 8.78535 9.22337 8.4768L14.6666 4.6665M4.53331 13.3332H11.4666C12.5868 13.3332 13.1468 13.3332 13.5746 13.1152C13.951 12.9234 14.2569 12.6175 14.4487 12.2412C14.6666 11.8133 14.6666 11.2533 14.6666 10.1332V5.8665C14.6666 4.7464 14.6666 4.18635 14.4487 3.75852C14.2569 3.3822 13.951 3.07624 13.5746 2.88449C13.1468 2.6665 12.5868 2.6665 11.4666 2.6665H4.53331C3.41321 2.6665 2.85316 2.6665 2.42533 2.88449C2.04901 3.07624 1.74305 3.3822 1.5513 3.75852C1.33331 4.18635 1.33331 4.7464 1.33331 5.8665V10.1332C1.33331 11.2533 1.33331 11.8133 1.5513 12.2412C1.74305 12.6175 2.04901 12.9234 2.42533 13.1152C2.85316 13.3332 3.41321 13.3332 4.53331 13.3332Z", "stroke", "#344054", "stroke-width", "1.5", "stroke-linecap", "round", "stroke-linejoin", "round"], ["d", "M10.6667 11.3333L14 8M14 8L10.6667 4.66667M14 8H6M6 2H5.2C4.0799 2 3.51984 2 3.09202 2.21799C2.7157 2.40973 2.40973 2.71569 2.21799 3.09202C2 3.51984 2 4.07989 2 5.2V10.8C2 11.9201 2 12.4802 2.21799 12.908C2.40973 13.2843 2.71569 13.5903 3.09202 13.782C3.51984 14 4.0799 14 5.2 14H6", "stroke", "#344054", "stroke-width", "1.5", "stroke-linecap", "round", "stroke-linejoin", "round"]],
      template: function HeaderComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "nav", 0)(1, "div", 1)(2, "ul", 2)(3, "li", 3)(4, "a", 4)(5, "strong", 5);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](6);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](7, "div", 6);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](8, HeaderComponent_div_8_Template, 6, 3, "div", 7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](9, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](10, HeaderComponent_div_10_Template, 6, 3, "div", 7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](11, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](12, HeaderComponent_div_12_Template, 6, 3, "div", 7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](13, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](14, "li", 8)(15, "a", 4)(16, "strong", 9);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](17, "Environment:");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](18, "strong");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](19);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](20, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](21, "ul", 10);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](22, HeaderComponent_ng_container_22_Template, 25, 6, "ng-container", 11);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](23, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](24, HeaderComponent_li_24_Template, 5, 2, "li", 12);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](25, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](26, HeaderComponent_ng_container_26_Template, 49, 12, "ng-container", 11);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](27, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
        }
        if (rf & 2) {
          let tmp_1_0;
          let tmp_2_0;
          let tmp_3_0;
          let tmp_4_0;
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](6);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"]((ctx.selectedApp == null ? null : ctx.selectedApp.title) || "Please select an application");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", (tmp_1_0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](9, 8, ctx.allowedAWSApps$)) == null ? null : tmp_1_0.length);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", (tmp_2_0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](11, 10, ctx.allowedAzureApps$)) == null ? null : tmp_2_0.length);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", (tmp_3_0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](13, 12, ctx.allowedGCPApps$)) == null ? null : tmp_3_0.length);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](((tmp_4_0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](20, 14, ctx.currentEnv$)) == null ? null : tmp_4_0.name) || "Please select an environment");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](23, 16, ctx.currentEnv$));
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](25, 18, ctx.environmentsTree$));
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](27, 20, ctx.user$));
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_9__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_9__.NgIf, _angular_router__WEBPACK_IMPORTED_MODULE_10__.RouterLink, _angular_common__WEBPACK_IMPORTED_MODULE_9__.NgOptimizedImage, _directives_dropdown_directive__WEBPACK_IMPORTED_MODULE_11__.DropdownDirective, _directives_submenu_directive__WEBPACK_IMPORTED_MODULE_12__.SubmenuDirective, _angular_common__WEBPACK_IMPORTED_MODULE_9__.AsyncPipe],
      styles: [".dropdown-menu[_ngcontent-%COMP%] {\n  overflow-y: auto;\n}\n.dropdown-menu.submenu[_ngcontent-%COMP%] {\n  position: fixed;\n}\n\n.application-menu[_ngcontent-%COMP%] {\n  max-width: 500px;\n}\n.application-menu[_ngcontent-%COMP%]   .dropdown-item[_ngcontent-%COMP%]   p.details[_ngcontent-%COMP%] {\n  white-space: normal;\n}\n\nnav[_ngcontent-%COMP%] {\n  height: 4.5rem;\n  left: initial;\n  border-bottom: 1px solid var(--gray-200, #EAECF0);\n  background-color: white;\n  padding: 0 24px;\n  position: sticky;\n  top: 0;\n  z-index: 1030;\n}\nnav[_ngcontent-%COMP%]   .user-picture[_ngcontent-%COMP%] {\n  border-radius: 50%;\n}\n\n.application-menu-new[_ngcontent-%COMP%] {\n  display: none;\n  position: absolute;\n  \n\n\n\n  padding: 2rem;\n  gap: 1.5rem;\n  flex: 1 0 0;\n  align-self: stretch;\n  border-radius: 12px;\n  border: 1px solid #EAECF0;\n  background: #FFF;\n  box-shadow: 0 4px 6px -2px rgba(16, 24, 40, 0.03), 0px 12px 16px -4px rgba(16, 24, 40, 0.08);\n}\n.application-menu-new.show[_ngcontent-%COMP%] {\n  display: flex;\n}\n.application-menu-new[_ngcontent-%COMP%]   .section[_ngcontent-%COMP%] {\n  display: flex;\n  width: 24rem;\n  flex-direction: column;\n  align-items: flex-start;\n  gap: 0.75rem;\n}\n.application-menu-new[_ngcontent-%COMP%]   .section[_ngcontent-%COMP%]   .header[_ngcontent-%COMP%] {\n  color: #196AAA;\n  font-size: 14px;\n  font-style: normal;\n  font-weight: 600;\n  line-height: 20px;\n}\n.application-menu-new[_ngcontent-%COMP%]   .section[_ngcontent-%COMP%]   .navigation[_ngcontent-%COMP%] {\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  gap: 0.5rem;\n  align-self: stretch;\n}\n.application-menu-new[_ngcontent-%COMP%]   .section[_ngcontent-%COMP%]   .navigation[_ngcontent-%COMP%]   .nav-item[_ngcontent-%COMP%] {\n  cursor: pointer;\n  display: flex;\n  padding: 0.75rem;\n  align-items: flex-start;\n  gap: 1rem;\n  align-self: stretch;\n  border-radius: 8px;\n}\n.application-menu-new[_ngcontent-%COMP%]   .section[_ngcontent-%COMP%]   .navigation[_ngcontent-%COMP%]   .nav-item[_ngcontent-%COMP%]   .description[_ngcontent-%COMP%] {\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  gap: 0.25rem;\n  align-self: stretch;\n}\n.application-menu-new[_ngcontent-%COMP%]   .section[_ngcontent-%COMP%]   .navigation[_ngcontent-%COMP%]   .nav-item[_ngcontent-%COMP%]   .description[_ngcontent-%COMP%]   span[_ngcontent-%COMP%]:first-child {\n  color: #101828;\n  font-size: 16px;\n  font-style: normal;\n  font-weight: 600;\n  line-height: 24px;\n}\n.application-menu-new[_ngcontent-%COMP%]   .section[_ngcontent-%COMP%]   .navigation[_ngcontent-%COMP%]   .nav-item[_ngcontent-%COMP%]   .description[_ngcontent-%COMP%]   span[_ngcontent-%COMP%] {\n  color: #475467;\n  font-size: 14px;\n  font-style: normal;\n  font-weight: 400;\n  line-height: 20px;\n}\n\n.blue[_ngcontent-%COMP%] {\n  font-size: 16px;\n  color: #1B75BB;\n  font-weight: 600;\n}\n\n.user-info[_ngcontent-%COMP%] {\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  gap: 0.75rem;\n}\n.user-info[_ngcontent-%COMP%]   div[_ngcontent-%COMP%] {\n  display: flex;\n  flex-direction: column;\n}\n.user-info[_ngcontent-%COMP%]   div[_ngcontent-%COMP%]   span[_ngcontent-%COMP%] {\n  font-size: 0.875rem;\n  line-height: 20px;\n  font-weight: 400;\n  color: #475467;\n}\n.user-info[_ngcontent-%COMP%]   div[_ngcontent-%COMP%]   span[_ngcontent-%COMP%]:first-child {\n  font-weight: 600;\n  color: #344054;\n}\n\n.env-info[_ngcontent-%COMP%] {\n  line-height: 20px;\n  font-weight: 400;\n  color: #475467;\n  font-size: 0.875rem;\n}\n.env-info[_ngcontent-%COMP%]   strong[_ngcontent-%COMP%] {\n  font-weight: 600;\n  color: #344054;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9oZWFkZXIvaGVhZGVyLmNvbXBvbmVudC5zY3NzIiwid2VicGFjazovLy4vc3JjL19nbG9iYWxzLnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBRUE7RUFDRSxnQkFBQTtBQURGO0FBR0U7RUFDRSxlQUFBO0FBREo7O0FBS0E7RUFDRSxnQkFBQTtBQUZGO0FBS0k7RUFDRSxtQkFBQTtBQUhOOztBQVFBO0VBQ0UsY0NwQmM7RURxQmQsYUFBQTtFQUNBLGlEQUFBO0VBQ0EsdUJBQUE7RUFDQSxlQUFBO0VBQ0EsZ0JBQUE7RUFDQSxNQUFBO0VBQ0EsYUFBQTtBQUxGO0FBT0U7RUFDRSxrQkFBQTtBQUxKOztBQVNBO0VBQ0UsYUFBQTtFQUNBLGtCQUFBO0VBQ0E7O0dBQUE7RUFHQSxhQUFBO0VBQ0EsV0FBQTtFQUNBLFdBQUE7RUFDQSxtQkFBQTtFQUNBLG1CQUFBO0VBQ0EseUJBQUE7RUFDQSxnQkFBQTtFQUNBLDRGQUFBO0FBTkY7QUFRRTtFQUNFLGFBQUE7QUFOSjtBQVNFO0VBQ0UsYUFBQTtFQUNBLFlBQUE7RUFDQSxzQkFBQTtFQUNBLHVCQUFBO0VBQ0EsWUFBQTtBQVBKO0FBU0k7RUFDRSxjQ3hEUTtFRHlEUixlQUFBO0VBQ0Esa0JBQUE7RUFDQSxnQkFBQTtFQUNBLGlCQUFBO0FBUE47QUFVSTtFQUNFLGFBQUE7RUFDQSxzQkFBQTtFQUNBLHVCQUFBO0VBQ0EsV0FBQTtFQUNBLG1CQUFBO0FBUk47QUFVTTtFQUNFLGVBQUE7RUFDQSxhQUFBO0VBQ0EsZ0JBQUE7RUFDQSx1QkFBQTtFQUNBLFNBQUE7RUFDQSxtQkFBQTtFQUNBLGtCQUFBO0FBUlI7QUFVUTtFQUNFLGFBQUE7RUFDQSxzQkFBQTtFQUNBLHVCQUFBO0VBQ0EsWUFBQTtFQUNBLG1CQUFBO0FBUlY7QUFVVTtFQUNFLGNDN0VEO0VEOEVDLGVBQUE7RUFDQSxrQkFBQTtFQUNBLGdCQUFBO0VBQ0EsaUJBQUE7QUFSWjtBQVdVO0VBQ0UsY0N4RkQ7RUR5RkMsZUFBQTtFQUNBLGtCQUFBO0VBQ0EsZ0JBQUE7RUFDQSxpQkFBQTtBQVRaOztBQWlCQTtFQUNFLGVBQUE7RUFDQSxjQzlHWTtFRCtHWixnQkFBQTtBQWRGOztBQWlCQTtFQUNFLGFBQUE7RUFDQSxtQkFBQTtFQUNBLHVCQUFBO0VBQ0EsWUFBQTtBQWRGO0FBZ0JFO0VBQ0UsYUFBQTtFQUNBLHNCQUFBO0FBZEo7QUFnQkk7RUFDRSxtQkFBQTtFQUNBLGlCQUFBO0VBQ0EsZ0JBQUE7RUFDQSxjQ3hISztBRDBHWDtBQWdCTTtFQUNFLGdCQUFBO0VBQ0EsY0MzSEc7QUQ2R1g7O0FBb0JBO0VBQ0UsaUJBQUE7RUFDQSxnQkFBQTtFQUNBLGNDcklTO0VEc0lULG1CQUFBO0FBakJGO0FBa0JFO0VBQ0UsZ0JBQUE7RUFDQSxjQ3hJTztBRHdIWCIsInNvdXJjZXNDb250ZW50IjpbIkB1c2UgXCIuLi8uLi8uLi9nbG9iYWxzXCI7XG5cbi5kcm9wZG93bi1tZW51IHtcbiAgb3ZlcmZsb3cteTogYXV0bztcblxuICAmLnN1Ym1lbnUge1xuICAgIHBvc2l0aW9uOiBmaXhlZDtcbiAgfVxufVxuXG4uYXBwbGljYXRpb24tbWVudSB7XG4gIG1heC13aWR0aDogNTAwcHg7XG5cbiAgLmRyb3Bkb3duLWl0ZW0ge1xuICAgIHAuZGV0YWlscyB7XG4gICAgICB3aGl0ZS1zcGFjZTogbm9ybWFsO1xuICAgIH1cbiAgfVxufVxuXG5uYXYge1xuICBoZWlnaHQ6IGdsb2JhbHMuJGhlYWRlci1oZWlnaHQ7XG4gIGxlZnQ6IGluaXRpYWw7XG4gIGJvcmRlci1ib3R0b206IDFweCBzb2xpZCB2YXIoLS1ncmF5LTIwMCwgI0VBRUNGMCk7XG4gIGJhY2tncm91bmQtY29sb3I6IHdoaXRlO1xuICBwYWRkaW5nOiAwIDI0cHg7XG4gIHBvc2l0aW9uOiBzdGlja3k7XG4gIHRvcDogMDtcbiAgei1pbmRleDogMTAzMDtcblxuICAudXNlci1waWN0dXJlIHtcbiAgICBib3JkZXItcmFkaXVzOiA1MCU7XG4gIH1cbn1cblxuLmFwcGxpY2F0aW9uLW1lbnUtbmV3IHtcbiAgZGlzcGxheTogbm9uZTtcbiAgcG9zaXRpb246IGFic29sdXRlO1xuICAvKlxuICB3aWR0aDogNjRyZW07XG4gICovXG4gIHBhZGRpbmc6IDJyZW07XG4gIGdhcDogMS41cmVtO1xuICBmbGV4OiAxIDAgMDtcbiAgYWxpZ24tc2VsZjogc3RyZXRjaDtcbiAgYm9yZGVyLXJhZGl1czogMTJweDtcbiAgYm9yZGVyOiAxcHggc29saWQgZ2xvYmFscy4kZ3JheS0yMDA7XG4gIGJhY2tncm91bmQ6ICNGRkY7XG4gIGJveC1zaGFkb3c6IDAgNHB4IDZweCAtMnB4IHJnYmEoMTYsIDI0LCA0MCwgMC4wMyksIDBweCAxMnB4IDE2cHggLTRweCByZ2JhKDE2LCAyNCwgNDAsIDAuMDgpO1xuXG4gICYuc2hvdyB7XG4gICAgZGlzcGxheTogZmxleDtcbiAgfVxuXG4gIC5zZWN0aW9uIHtcbiAgICBkaXNwbGF5OiBmbGV4O1xuICAgIHdpZHRoOiAyNHJlbTtcbiAgICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICAgIGFsaWduLWl0ZW1zOiBmbGV4LXN0YXJ0O1xuICAgIGdhcDogLjc1cmVtO1xuXG4gICAgLmhlYWRlciB7XG4gICAgICBjb2xvcjogZ2xvYmFscy4kcHJpbWFyeS02MDA7XG4gICAgICBmb250LXNpemU6IDE0cHg7XG4gICAgICBmb250LXN0eWxlOiBub3JtYWw7XG4gICAgICBmb250LXdlaWdodDogNjAwO1xuICAgICAgbGluZS1oZWlnaHQ6IDIwcHg7XG4gICAgfVxuXG4gICAgLm5hdmlnYXRpb24ge1xuICAgICAgZGlzcGxheTogZmxleDtcbiAgICAgIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XG4gICAgICBhbGlnbi1pdGVtczogZmxleC1zdGFydDtcbiAgICAgIGdhcDogLjVyZW07XG4gICAgICBhbGlnbi1zZWxmOiBzdHJldGNoO1xuXG4gICAgICAubmF2LWl0ZW0ge1xuICAgICAgICBjdXJzb3I6IHBvaW50ZXI7XG4gICAgICAgIGRpc3BsYXk6IGZsZXg7XG4gICAgICAgIHBhZGRpbmc6IC43NXJlbTtcbiAgICAgICAgYWxpZ24taXRlbXM6IGZsZXgtc3RhcnQ7XG4gICAgICAgIGdhcDogMXJlbTtcbiAgICAgICAgYWxpZ24tc2VsZjogc3RyZXRjaDtcbiAgICAgICAgYm9yZGVyLXJhZGl1czogOHB4O1xuXG4gICAgICAgIC5kZXNjcmlwdGlvbiB7XG4gICAgICAgICAgZGlzcGxheTogZmxleDtcbiAgICAgICAgICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICAgICAgICAgIGFsaWduLWl0ZW1zOiBmbGV4LXN0YXJ0O1xuICAgICAgICAgIGdhcDogLjI1cmVtO1xuICAgICAgICAgIGFsaWduLXNlbGY6IHN0cmV0Y2g7XG5cbiAgICAgICAgICBzcGFuOmZpcnN0LWNoaWxkIHtcbiAgICAgICAgICAgIGNvbG9yOiBnbG9iYWxzLiRncmF5LTkwMDtcbiAgICAgICAgICAgIGZvbnQtc2l6ZTogMTZweDtcbiAgICAgICAgICAgIGZvbnQtc3R5bGU6IG5vcm1hbDtcbiAgICAgICAgICAgIGZvbnQtd2VpZ2h0OiA2MDA7XG4gICAgICAgICAgICBsaW5lLWhlaWdodDogMjRweDtcbiAgICAgICAgICB9XG5cbiAgICAgICAgICBzcGFuIHtcbiAgICAgICAgICAgIGNvbG9yOiBnbG9iYWxzLiRncmF5LTYwMDtcbiAgICAgICAgICAgIGZvbnQtc2l6ZTogMTRweDtcbiAgICAgICAgICAgIGZvbnQtc3R5bGU6IG5vcm1hbDtcbiAgICAgICAgICAgIGZvbnQtd2VpZ2h0OiA0MDA7XG4gICAgICAgICAgICBsaW5lLWhlaWdodDogMjBweDtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gIH1cbn1cblxuLmJsdWUge1xuICBmb250LXNpemU6IDE2cHg7XG4gIGNvbG9yOiBnbG9iYWxzLiRwcmltYXJ5LTUwMDtcbiAgZm9udC13ZWlnaHQ6IDYwMDtcbn1cblxuLnVzZXItaW5mbyB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIGp1c3RpZnktY29udGVudDogY2VudGVyO1xuICBnYXA6IC43NXJlbTtcblxuICBkaXYge1xuICAgIGRpc3BsYXk6IGZsZXg7XG4gICAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjtcblxuICAgIHNwYW4ge1xuICAgICAgZm9udC1zaXplOiAwLjg3NXJlbTtcbiAgICAgIGxpbmUtaGVpZ2h0OiAyMHB4O1xuICAgICAgZm9udC13ZWlnaHQ6IDQwMDtcbiAgICAgIGNvbG9yOiBnbG9iYWxzLiRncmF5LTYwMDtcblxuICAgICAgJjpmaXJzdC1jaGlsZCB7XG4gICAgICAgIGZvbnQtd2VpZ2h0OiA2MDA7XG4gICAgICAgIGNvbG9yOiBnbG9iYWxzLiRncmF5LTcwMDtcbiAgICAgIH1cbiAgICB9XG4gIH1cbn1cblxuLmVudi1pbmZvIHtcbiAgbGluZS1oZWlnaHQ6IDIwcHg7XG4gIGZvbnQtd2VpZ2h0OiA0MDA7XG4gIGNvbG9yOiBnbG9iYWxzLiRncmF5LTYwMDtcbiAgZm9udC1zaXplOiAwLjg3NXJlbTtcbiAgc3Ryb25nIHtcbiAgICBmb250LXdlaWdodDogNjAwO1xuICAgIGNvbG9yOiBnbG9iYWxzLiRncmF5LTcwMDtcbiAgfVxufVxuIiwiJGZvbnQtZmFtaWx5LWJhc2U6IEludGVyLCBzYW5zLXNlcmlmO1xuJGhlYWRlci1oZWlnaHQ6IDQuNXJlbTtcbiRmb290ZXItaGVpZ2h0OiA1LjVyZW07XG5cbiRwcmltYXJ5LTIwMDogIzk2QzBFMDtcbiRwcmltYXJ5LTUwMDogIzFCNzVCQjtcbiRwcmltYXJ5LTYwMDogIzE5NkFBQTtcbiRwcmltYXJ5LTcwMDogIzEzNTM4NTtcblxuJGdyYXktNTA6ICNGOUZBRkI7XG4kZ3JheS0xMDA6ICNGMkY0Rjc7XG4kZ3JheS0yMDA6ICNFQUVDRjA7XG4kZ3JheS0zMDA6ICNEMEQ1REQ7XG4kZ3JheS02MDA6ICM0NzU0Njc7XG4kZ3JheS03MDA6ICMzNDQwNTQ7XG4kZ3JheS04MDA6ICMxRDI5Mzk7XG4kZ3JheS05MDA6ICMxMDE4Mjg7XG5cblxuJGxpbmstY29sb3I6ICRwcmltYXJ5LTUwMCAhZGVmYXVsdDtcblxuQG1peGluIGhpZGUtc2Nyb2xsYmFycyB7XG4gIHNjcm9sbGJhci13aWR0aDogbm9uZTtcbiAgLW1zLW92ZXJmbG93LXN0eWxlOiBub25lO1xuICAmOjotd2Via2l0LXNjcm9sbGJhciB7XG4gICAgZGlzcGxheTogbm9uZTtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return HeaderComponent;
})();

/***/ }),

/***/ 159:
/*!***************************************************!*\
  !*** ./src/app/components/home/home.component.ts ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   HomeComponent: () => (/* binding */ HomeComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_template_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../services/template.service */ 529);
/* harmony import */ var _services_environment_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../services/environment.service */ 1574);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _dashboard_components_dashboard_dashboard_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../dashboard/components/dashboard/dashboard.component */ 5863);
/* harmony import */ var _layout_layout_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../layout/layout.component */ 2952);






const _c0 = function () {
  return [];
};
function HomeComponent_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "theia-dashboard", 1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("rows", (ctx_r0.currentAction == null ? null : ctx_r0.currentAction.rows) || _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction0"](1, _c0));
  }
}
let HomeComponent = /*#__PURE__*/(() => {
  class HomeComponent {
    constructor(templateService, environmentService) {
      this.templateService = templateService;
      this.currentEnv$ = environmentService.getCurrentEnvironment();
    }
    ngOnInit() {
      this.currentAction = this.templateService.getActionById('home', 'dashboard');
    }
    static #_ = this.ɵfac = function HomeComponent_Factory(t) {
      return new (t || HomeComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_template_service__WEBPACK_IMPORTED_MODULE_1__.TemplateService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_environment_service__WEBPACK_IMPORTED_MODULE_2__.EnvironmentService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: HomeComponent,
      selectors: [["theia-home"]],
      decls: 3,
      vars: 3,
      consts: [[4, "ngIf"], [1, "row", 3, "rows"]],
      template: function HomeComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "theia-layout");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, HomeComponent_ng_container_1_Template, 2, 2, "ng-container", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](2, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](2, 1, ctx.currentEnv$) || (ctx.currentAction == null ? null : ctx.currentAction.env_not_required));
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_3__.NgIf, _dashboard_components_dashboard_dashboard_component__WEBPACK_IMPORTED_MODULE_4__.DashboardComponent, _layout_layout_component__WEBPACK_IMPORTED_MODULE_5__.LayoutComponent, _angular_common__WEBPACK_IMPORTED_MODULE_3__.AsyncPipe],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return HomeComponent;
})();

/***/ }),

/***/ 3636:
/*!***************************************************!*\
  !*** ./src/app/components/info/info.component.ts ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   InfoComponent: () => (/* binding */ InfoComponent)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ 8071);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_info_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../services/info.service */ 957);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var ngx_markdown__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ngx-markdown */ 1995);





function InfoComponent_i_0_Template(rf, ctx) {
  if (rf & 1) {
    const _r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "i", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function InfoComponent_i_0_Template_i_click_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r2);
      const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r1.openInfo());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
let InfoComponent = /*#__PURE__*/(() => {
  class InfoComponent {
    constructor(infoService) {
      this.infoService = infoService;
      this.data$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject('');
      this.enabled$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject(false);
      this.collapsed = false;
      this.animating = false;
      this.data$ = infoService.data$;
      this.enabled$ = infoService.enabled$;
    }
    ngOnInit() {
      this.enabled$.subscribe(value => {
        this.animating = true;
        this.collapsed = !value;
        setTimeout(() => {
          this.animating = false;
        }, 250);
      });
    }
    close() {
      this.infoService.enabled = false;
    }
    openInfo() {
      this.infoService.enabled = true;
    }
    static #_ = this.ɵfac = function InfoComponent_Factory(t) {
      return new (t || InfoComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_info_service__WEBPACK_IMPORTED_MODULE_2__.InfoService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: InfoComponent,
      selectors: [["theia-info"]],
      hostVars: 4,
      hostBindings: function InfoComponent_HostBindings(rf, ctx) {
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵclassProp"]("collapsed", ctx.collapsed)("animating", ctx.animating);
        }
      },
      decls: 8,
      vars: 8,
      consts: [["class", "info-btn bi bi-info-circle fs-5", 3, "click", 4, "ngIf"], [1, "info-panel", "border-bottom"], [1, "close-wrapper"], ["type", "button", "data-bs-dismiss", "modal", "aria-label", "Close", 1, "btn-close", 3, "click"], [3, "innerHTML"], [1, "info-btn", "bi", "bi-info-circle", "fs-5", 3, "click"]],
      template: function InfoComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](0, InfoComponent_i_0_Template, 1, 0, "i", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](1, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "div", 1)(3, "div", 2)(4, "button", 3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function InfoComponent_Template_button_click_4_listener() {
            return ctx.close();
          });
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](5, "div", 4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](6, "markdown");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](7, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](1, 2, ctx.enabled$) === false);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](5);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("innerHTML", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](6, 4, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](7, 6, ctx.data$) || ""), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsanitizeHtml"]);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_3__.NgIf, _angular_common__WEBPACK_IMPORTED_MODULE_3__.AsyncPipe, ngx_markdown__WEBPACK_IMPORTED_MODULE_4__.MarkdownPipe],
      styles: ["[_nghost-%COMP%] {\n  padding-right: 0;\n  padding-left: 0;\n  margin-left: 1rem;\n  max-width: 19rem;\n  transition: 0.15s ease-in;\n  position: relative;\n  overflow: hidden;\n}\n[_nghost-%COMP%]   .info-btn[_ngcontent-%COMP%] {\n  position: absolute;\n  left: 0.6rem;\n  top: 0.2rem;\n}\n\n.info-panel[_ngcontent-%COMP%] {\n  background-color: white;\n  z-index: 10;\n  padding: 1rem;\n  position: relative;\n  overflow: auto;\n  border-radius: 8px;\n  border: 1px solid #EAECF0;\n  transform: translateX(0);\n  transition: 0.25s ease-in;\n}\n.info-panel[_ngcontent-%COMP%]   .close-wrapper[_ngcontent-%COMP%] {\n  position: sticky;\n  top: 0;\n}\n.info-panel[_ngcontent-%COMP%]   .btn-close[_ngcontent-%COMP%] {\n  position: absolute;\n  right: -0.75rem;\n  top: -0.75rem;\n  cursor: pointer;\n  width: 1.25rem;\n  height: 1.25rem;\n}\n\n.collapsed[_nghost-%COMP%] {\n  width: 2rem;\n  height: 1.5rem;\n  margin-left: 0;\n  transition: 0.15s ease-out;\n  scrollbar-width: none;\n  -ms-overflow-style: none;\n}\n.collapsed[_nghost-%COMP%]::-webkit-scrollbar {\n  display: none;\n}\n.collapsed[_nghost-%COMP%]   .info-panel[_ngcontent-%COMP%] {\n  transform: translateX(20.67rem);\n  transition: 0.25s ease-out;\n}\n\n.animating[_nghost-%COMP%] {\n  scrollbar-width: none;\n  -ms-overflow-style: none;\n}\n.animating[_nghost-%COMP%]::-webkit-scrollbar {\n  display: none;\n}\n.animating[_nghost-%COMP%]   .info-btn[_ngcontent-%COMP%] {\n  display: none;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9pbmZvL2luZm8uY29tcG9uZW50LnNjc3MiLCJ3ZWJwYWNrOi8vLi9zcmMvX2dsb2JhbHMuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFFQTtFQUNFLGdCQUFBO0VBQ0EsZUFBQTtFQUNBLGlCQUFBO0VBQ0EsZ0JBQUE7RUFDQSx5QkFBQTtFQUNBLGtCQUFBO0VBQ0EsZ0JBQUE7QUFERjtBQUdFO0VBQ0Usa0JBQUE7RUFDQSxZQUFBO0VBQ0EsV0FBQTtBQURKOztBQU1BO0VBQ0UsdUJBQUE7RUFDQSxXQUFBO0VBQ0EsYUFBQTtFQUNBLGtCQUFBO0VBQ0EsY0FBQTtFQUVBLGtCQUFBO0VBQ0EseUJBQUE7RUFFQSx3QkFBQTtFQUNBLHlCQUFBO0FBTEY7QUFPRTtFQUNFLGdCQUFBO0VBQ0EsTUFBQTtBQUxKO0FBUUU7RUFDRSxrQkFBQTtFQUNBLGVBQUE7RUFDQSxhQUFBO0VBQ0EsZUFBQTtFQUNBLGNBQUE7RUFDQSxlQUFBO0FBTko7O0FBVUE7RUFDRSxXQUFBO0VBQ0EsY0FBQTtFQUNBLGNBQUE7RUFDQSwwQkFBQTtFQzdCQSxxQkFBQTtFQUNBLHdCQUFBO0FEdUJGO0FDdEJFO0VBQ0UsYUFBQTtBRHdCSjtBQUtDO0VBQ0csK0JBQUE7RUFDQSwwQkFBQTtBQUhKOztBQVFBO0VDdkNFLHFCQUFBO0VBQ0Esd0JBQUE7QURtQ0Y7QUNsQ0U7RUFDRSxhQUFBO0FEb0NKO0FBRUU7RUFDRSxhQUFBO0FBQUoiLCJzb3VyY2VzQ29udGVudCI6WyJAdXNlIFwiLi4vLi4vLi4vZ2xvYmFsc1wiO1xuXG46aG9zdCB7XG4gIHBhZGRpbmctcmlnaHQ6IDA7XG4gIHBhZGRpbmctbGVmdDogMDtcbiAgbWFyZ2luLWxlZnQ6IDFyZW07XG4gIG1heC13aWR0aDogMTlyZW07XG4gIHRyYW5zaXRpb246IC4xNXMgZWFzZS1pbjtcbiAgcG9zaXRpb246IHJlbGF0aXZlO1xuICBvdmVyZmxvdzogaGlkZGVuO1xuXG4gIC5pbmZvLWJ0biB7XG4gICAgcG9zaXRpb246IGFic29sdXRlO1xuICAgIGxlZnQ6IC42cmVtO1xuICAgIHRvcDogMC4ycmVtO1xuICB9XG5cbn1cblxuLmluZm8tcGFuZWwge1xuICBiYWNrZ3JvdW5kLWNvbG9yOiB3aGl0ZTtcbiAgei1pbmRleDogMTA7XG4gIHBhZGRpbmc6IDFyZW07XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgb3ZlcmZsb3c6IGF1dG87XG5cbiAgYm9yZGVyLXJhZGl1czogOHB4O1xuICBib3JkZXI6IDFweCBzb2xpZCBnbG9iYWxzLiRncmF5LTIwMDtcblxuICB0cmFuc2Zvcm06IHRyYW5zbGF0ZVgoMCk7XG4gIHRyYW5zaXRpb246IC4yNXMgZWFzZS1pbjtcblxuICAuY2xvc2Utd3JhcHBlciB7XG4gICAgcG9zaXRpb246IHN0aWNreTtcbiAgICB0b3A6IDA7XG4gIH1cblxuICAuYnRuLWNsb3NlIHtcbiAgICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gICAgcmlnaHQ6IC0uNzVyZW07XG4gICAgdG9wOiAtLjc1cmVtO1xuICAgIGN1cnNvcjogcG9pbnRlcjtcbiAgICB3aWR0aDogMS4yNXJlbTtcbiAgICBoZWlnaHQ6IDEuMjVyZW07XG4gIH1cbn1cblxuOmhvc3QoLmNvbGxhcHNlZCkge1xuICB3aWR0aDogMnJlbTtcbiAgaGVpZ2h0OiAxLjVyZW07XG4gIG1hcmdpbi1sZWZ0OiAwO1xuICB0cmFuc2l0aW9uOiAuMTVzIGVhc2Utb3V0O1xuICBAaW5jbHVkZSBnbG9iYWxzLmhpZGUtc2Nyb2xsYmFycztcblxuIC5pbmZvLXBhbmVsIHtcbiAgICB0cmFuc2Zvcm06IHRyYW5zbGF0ZVgoMjAuNjdyZW0pO1xuICAgIHRyYW5zaXRpb246IC4yNXMgZWFzZS1vdXQ7XG4gIH1cblxufVxuXG46aG9zdCguYW5pbWF0aW5nKSB7XG4gIEBpbmNsdWRlIGdsb2JhbHMuaGlkZS1zY3JvbGxiYXJzO1xuICAuaW5mby1idG4ge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cbn1cbiIsIiRmb250LWZhbWlseS1iYXNlOiBJbnRlciwgc2Fucy1zZXJpZjtcbiRoZWFkZXItaGVpZ2h0OiA0LjVyZW07XG4kZm9vdGVyLWhlaWdodDogNS41cmVtO1xuXG4kcHJpbWFyeS0yMDA6ICM5NkMwRTA7XG4kcHJpbWFyeS01MDA6ICMxQjc1QkI7XG4kcHJpbWFyeS02MDA6ICMxOTZBQUE7XG4kcHJpbWFyeS03MDA6ICMxMzUzODU7XG5cbiRncmF5LTUwOiAjRjlGQUZCO1xuJGdyYXktMTAwOiAjRjJGNEY3O1xuJGdyYXktMjAwOiAjRUFFQ0YwO1xuJGdyYXktMzAwOiAjRDBENUREO1xuJGdyYXktNjAwOiAjNDc1NDY3O1xuJGdyYXktNzAwOiAjMzQ0MDU0O1xuJGdyYXktODAwOiAjMUQyOTM5O1xuJGdyYXktOTAwOiAjMTAxODI4O1xuXG5cbiRsaW5rLWNvbG9yOiAkcHJpbWFyeS01MDAgIWRlZmF1bHQ7XG5cbkBtaXhpbiBoaWRlLXNjcm9sbGJhcnMge1xuICBzY3JvbGxiYXItd2lkdGg6IG5vbmU7XG4gIC1tcy1vdmVyZmxvdy1zdHlsZTogbm9uZTtcbiAgJjo6LXdlYmtpdC1zY3JvbGxiYXIge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cbn1cbiJdLCJzb3VyY2VSb290IjoiIn0= */"]
    });
  }
  return InfoComponent;
})();

/***/ }),

/***/ 1052:
/*!***************************************************************************!*\
  !*** ./src/app/components/key-value-editor/key-value-editor.component.ts ***!
  \***************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   KeyValueEditorComponent: () => (/* binding */ KeyValueEditorComponent)
/* harmony export */ });
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/forms */ 8849);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ 6575);




function KeyValueEditorComponent_div_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 3)(1, "div", 4)(2, "span", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](3, "Loading...");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
  }
}
function KeyValueEditorComponent_ng_template_2_ng_container_0_div_1_label_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "label", 21);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r9 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](ctx_r9.keyLabel || "Key");
  }
}
function KeyValueEditorComponent_ng_template_2_ng_container_0_div_1_label_9_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "label", 21);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r10 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](ctx_r10.valueLabel || "Value");
  }
}
const _c0 = function (a0) {
  return {
    "is-invalid": a0
  };
};
const _c1 = function (a0) {
  return {
    "first-row": a0
  };
};
function KeyValueEditorComponent_ng_template_2_ng_container_0_div_1_Template(rf, ctx) {
  if (rf & 1) {
    const _r12 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 10)(1, "div", 11)(2, "div", 12)(3, "div", 13);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, KeyValueEditorComponent_ng_template_2_ng_container_0_div_1_label_4_Template, 2, 1, "label", 14);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](5, "input", 15);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](6, "div", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](8, "div", 13);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](9, KeyValueEditorComponent_ng_template_2_ng_container_0_div_1_label_9_Template, 2, 1, "label", 14);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](10, "input", 17);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](11, "div", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](12);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](13, "div", 18)(14, "button", 19);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function KeyValueEditorComponent_ng_template_2_ng_container_0_div_1_Template_button_click_14_listener() {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r12);
      const index_r7 = restoredCtx.index;
      const ctx_r11 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r11.deleteRow(index_r7));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](15, "i", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
  }
  if (rf & 2) {
    const pair_r6 = ctx.$implicit;
    const first_r8 = ctx.first;
    const ctx_r5 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formGroup", pair_r6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", first_r8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx_r5.readonly)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](11, _c0, ctx_r5.isInvalid(pair_r6, "key")));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", ctx_r5.errorMessage(pair_r6, "key"), " ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", first_r8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx_r5.readonly)("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](13, _c0, ctx_r5.isInvalid(pair_r6, "value")));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", ctx_r5.errorMessage(pair_r6, "value"), " ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](15, _c1, first_r8));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx_r5.readonly);
  }
}
function KeyValueEditorComponent_ng_template_2_ng_container_0_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, KeyValueEditorComponent_ng_template_2_ng_container_0_div_1_Template, 16, 17, "div", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r3.pairs);
  }
}
function KeyValueEditorComponent_ng_template_2_div_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 10)(1, "div", 22);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2, " Use the button below to add new values ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
}
function KeyValueEditorComponent_ng_template_2_Template(rf, ctx) {
  if (rf & 1) {
    const _r14 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](0, KeyValueEditorComponent_ng_template_2_ng_container_0_Template, 2, 1, "ng-container", 6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, KeyValueEditorComponent_ng_template_2_div_1_Template, 3, 0, "div", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "button", 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function KeyValueEditorComponent_ng_template_2_Template_button_click_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r14);
      const ctx_r13 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r13.addRow());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r2.pairs.length);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !ctx_r2.pairs.length);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx_r2.readonly);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](ctx_r2.addLabel || "Add value");
  }
}
let KeyValueEditorComponent = /*#__PURE__*/(() => {
  class KeyValueEditorComponent {
    set value(val) {
      if (val) {
        const parsed = JSON.parse(val);
        this.control.setValue([]);
        for (const [key, val] of Object.entries(parsed)) {
          this.addRow(key, val);
        }
      }
    }
    constructor(fb) {
      this.fb = fb;
      this.isDisabled = false;
      this.parent = new _angular_forms__WEBPACK_IMPORTED_MODULE_1__.UntypedFormGroup({});
      this.id = '';
      this.readonly = false;
      this.addLabel = 'Add value';
      this.keyLabel = 'Key';
      this.valueLabel = 'Value';
      this.loading = false;
    }
    get control() {
      return this.parent.get(this.id);
    }
    get pairs() {
      return this.control.controls;
    }
    ngOnInit() {
      this.parent.setControl(this.id, this.fb.array([]));
    }
    uniqueValidator(name) {
      return control => {
        const formArray = control?.parent?.parent;
        if (!formArray) {
          return null;
        }
        for (const group of formArray.controls) {
          const otherControl = group.get(name);
          if (otherControl?.value === control?.value && control !== otherControl) {
            return {
              unique: true
            };
          }
        }
        return null;
      };
    }
    addRow(key = '', value = '') {
      this.control.push(this.fb.group({
        key: [key, [_angular_forms__WEBPACK_IMPORTED_MODULE_1__.Validators.required, this.uniqueValidator('key')]],
        value: [value, _angular_forms__WEBPACK_IMPORTED_MODULE_1__.Validators.required]
      }));
    }
    deleteRow(index) {
      this.control.removeAt(index);
      for (const control of this.control.controls) {
        // check for unique keys
        control.get('key')?.updateValueAndValidity();
      }
    }
    isInvalid(group, name) {
      const control = group.get(name);
      return !!((control?.touched || control?.dirty) && control?.invalid);
    }
    errorMessage(group, name) {
      const control = group.get(name);
      let result = '';
      if (control?.hasError('required')) {
        result = 'This field is required.';
      } else if (control?.hasError('unique')) {
        result = 'Keys must be unique.';
      }
      return result;
    }
    static #_ = this.ɵfac = function KeyValueEditorComponent_Factory(t) {
      return new (t || KeyValueEditorComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_forms__WEBPACK_IMPORTED_MODULE_1__.UntypedFormBuilder));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: KeyValueEditorComponent,
      selectors: [["theia-key-value-editor"]],
      inputs: {
        parent: "parent",
        id: "id",
        readonly: "readonly",
        addLabel: "addLabel",
        keyLabel: "keyLabel",
        valueLabel: "valueLabel",
        loading: "loading",
        value: "value"
      },
      decls: 4,
      vars: 2,
      consts: [[1, "mb-3"], ["class", "d-flex justify-content-center loader", 4, "ngIf", "ngIfElse"], ["loaded", ""], [1, "d-flex", "justify-content-center", "loader"], ["role", "status", 1, "spinner-border", "spinner-big", "text-primary"], [1, "visually-hidden"], [4, "ngIf"], ["class", "row mb-2", 4, "ngIf"], [1, "btn", "btn-outline-secondary", "btn-sm", 3, "disabled", "click"], ["class", "row mb-2", 4, "ngFor", "ngForOf"], [1, "row", "mb-2"], [1, "col-11"], [1, "row", 3, "formGroup"], [1, "col-6"], ["class", "form-label", 4, "ngIf"], ["type", "text", "formControlName", "key", 1, "form-control", "form-control-sm", 3, "disabled", "ngClass"], [1, "invalid-feedback"], ["type", "text", "formControlName", "value", 1, "form-control", "form-control-sm", 3, "disabled", "ngClass"], [1, "col-1", 3, "ngClass"], [1, "btn", "btn-outline-danger", "btn-sm", 3, "disabled", "click"], [1, "bi", "bi-trash"], [1, "form-label"], [1, "col", "text-muted"]],
      template: function KeyValueEditorComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, KeyValueEditorComponent_div_1_Template, 4, 0, "div", 1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, KeyValueEditorComponent_ng_template_2_Template, 4, 4, "ng-template", null, 2, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplateRefExtractor"]);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }
        if (rf & 2) {
          const _r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.loading)("ngIfElse", _r1);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_2__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_2__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_2__.NgIf, _angular_forms__WEBPACK_IMPORTED_MODULE_1__.DefaultValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_1__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_1__.NgControlStatusGroup, _angular_forms__WEBPACK_IMPORTED_MODULE_1__.FormGroupDirective, _angular_forms__WEBPACK_IMPORTED_MODULE_1__.FormControlName],
      styles: [".first-row[_ngcontent-%COMP%] {\n  padding-top: 2rem;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9rZXktdmFsdWUtZWRpdG9yL2tleS12YWx1ZS1lZGl0b3IuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxpQkFBQTtBQUNGIiwic291cmNlc0NvbnRlbnQiOlsiLmZpcnN0LXJvdyB7XG4gIHBhZGRpbmctdG9wOiAycmVtO1xufVxuIl0sInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return KeyValueEditorComponent;
})();

/***/ }),

/***/ 2952:
/*!*******************************************************!*\
  !*** ./src/app/components/layout/layout.component.ts ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   LayoutComponent: () => (/* binding */ LayoutComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_environment_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../services/environment.service */ 1574);
/* harmony import */ var _header_header_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../header/header.component */ 6471);
/* harmony import */ var _footer_footer_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../footer/footer.component */ 7913);
/* harmony import */ var _sidebar_sidebar_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../sidebar/sidebar.component */ 7954);





const _c0 = ["*"];
let LayoutComponent = /*#__PURE__*/(() => {
  class LayoutComponent {
    constructor(environmentService) {
      this.environmentService = environmentService;
      this.currentEnv$ = environmentService.getCurrentEnvironment();
    }
    static #_ = this.ɵfac = function LayoutComponent_Factory(t) {
      return new (t || LayoutComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_environment_service__WEBPACK_IMPORTED_MODULE_1__.EnvironmentService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: LayoutComponent,
      selectors: [["theia-layout"]],
      ngContentSelectors: _c0,
      decls: 8,
      vars: 0,
      consts: [[1, "container-fluid"], [1, "row", "flex-nowrap"], [1, ""], [1, "flex-grow-1", "flex-shrink-1", "border-end"], [1, "content"]],
      template: function LayoutComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵprojectionDef"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "main", 0)(1, "div", 1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](2, "theia-sidebar", 2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "section", 3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](4, "theia-header");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "div", 4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵprojection"](6);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](7, "theia-footer");
        }
      },
      dependencies: [_header_header_component__WEBPACK_IMPORTED_MODULE_2__.HeaderComponent, _footer_footer_component__WEBPACK_IMPORTED_MODULE_3__.FooterComponent, _sidebar_sidebar_component__WEBPACK_IMPORTED_MODULE_4__.SidebarComponent],
      styles: ["main[_ngcontent-%COMP%] {\n  position: relative;\n}\n\nsection[_ngcontent-%COMP%] {\n  height: calc(100vh - 5.5rem);\n  overflow: auto;\n  padding: 0;\n}\nsection[_ngcontent-%COMP%]    > div[_ngcontent-%COMP%] {\n  font-size: 14px;\n  padding: 1rem 1.5rem;\n  height: calc(100vh - 4.5rem - 5.5rem - 1.8rem);\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9sYXlvdXQvbGF5b3V0LmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUVBO0VBRUUsa0JBQUE7QUFGRjs7QUFLQTtFQUNFLDRCQUFBO0VBQ0EsY0FBQTtFQUNBLFVBQUE7QUFGRjtBQUdFO0VBQ0UsZUFBQTtFQUNBLG9CQUFBO0VBQ0EsOENBQUE7QUFESiIsInNvdXJjZXNDb250ZW50IjpbIkB1c2UgXCIuLi8uLi8uLi9nbG9iYWxzXCI7XG5cbm1haW4ge1xuICAvL21hcmdpbi10b3A6IGdsb2JhbHMuJGhlYWRlci1oZWlnaHQ7XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcbn1cblxuc2VjdGlvbiB7XG4gIGhlaWdodDogY2FsYygxMDB2aCAtICN7Z2xvYmFscy4kZm9vdGVyLWhlaWdodH0pO1xuICBvdmVyZmxvdzogYXV0bztcbiAgcGFkZGluZzogMDtcbiAgJiA+IGRpdiB7XG4gICAgZm9udC1zaXplOiAxNHB4O1xuICAgIHBhZGRpbmc6IDFyZW0gMS41cmVtO1xuICAgIGhlaWdodDogY2FsYygxMDB2aCAtIDQuNXJlbSAtIDUuNXJlbSAtIDEuOHJlbSk7XG5cbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return LayoutComponent;
})();

/***/ }),

/***/ 354:
/*!*****************************************************!*\
  !*** ./src/app/components/modal/modal.component.ts ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ModalComponent: () => (/* binding */ ModalComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ 6575);


function ModalComponent_div_9_Template(rf, ctx) {
  if (rf & 1) {
    const _r2 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function ModalComponent_div_9_Template_div_click_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r2);
      const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r1.clickOut());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
const _c0 = [[["", "slot", "header"]], [["", "slot", "body"]], [["", "slot", "footer"]]];
const _c1 = function (a0) {
  return {
    "show": a0
  };
};
const _c2 = ["[slot=header]", "[slot=body]", "[slot=footer]"];
let ModalComponent = /*#__PURE__*/(() => {
  class ModalComponent {
    constructor() {
      this.visible = false;
      this.classes = '';
    }
    clickOut() {
      this.visible = false;
    }
    static #_ = this.ɵfac = function ModalComponent_Factory(t) {
      return new (t || ModalComponent)();
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: ModalComponent,
      selectors: [["theia-modal"]],
      inputs: {
        visible: "visible",
        classes: "classes"
      },
      ngContentSelectors: _c2,
      decls: 10,
      vars: 5,
      consts: [["tabindex", "-1", 1, "modal", "fade", "show", 3, "ngClass"], [1, "modal-dialog", 3, "ngClass"], [1, "modal-content"], [1, "modal-header"], [1, "modal-body", "text-start"], [1, "modal-footer", "d-flex"], ["class", "modal-backdrop fade show", 3, "click", 4, "ngIf"], [1, "modal-backdrop", "fade", "show", 3, "click"]],
      template: function ModalComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵprojectionDef"](_c0);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 0)(1, "div", 1)(2, "div", 2)(3, "div", 3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵprojection"](4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "div", 4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵprojection"](6, 1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](7, "div", 5);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵprojection"](8, 2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](9, ModalComponent_div_9_Template, 1, 0, "div", 6);
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](3, _c1, ctx.visible));
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", ctx.classes);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](8);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.visible);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_1__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_1__.NgIf],
      styles: [".show[_ngcontent-%COMP%] {\n  display: block;\n}\n\n.modal-header[_ngcontent-%COMP%] {\n  border-bottom: 0;\n}\n\n.modal-body[_ngcontent-%COMP%] {\n  font-weight: 400;\n  color: #475467;\n}\n\n.modal-footer[_ngcontent-%COMP%] {\n  border-top: 0;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9tb2RhbC9tb2RhbC5jb21wb25lbnQuc2NzcyIsIndlYnBhY2s6Ly8uL3NyYy9fZ2xvYmFscy5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUVBO0VBQ0UsY0FBQTtBQURGOztBQUlBO0VBQ0UsZ0JBQUE7QUFERjs7QUFJQTtFQUNFLGdCQUFBO0VBQ0EsY0NDUztBREZYOztBQUlBO0VBQ0UsYUFBQTtBQURGIiwic291cmNlc0NvbnRlbnQiOlsiQHVzZSBcIi4uLy4uLy4uL2dsb2JhbHNcIjtcblxuLnNob3cge1xuICBkaXNwbGF5OiBibG9jaztcbn1cblxuLm1vZGFsLWhlYWRlciB7XG4gIGJvcmRlci1ib3R0b206IDA7XG59XG5cbi5tb2RhbC1ib2R5IHtcbiAgZm9udC13ZWlnaHQ6IDQwMDtcbiAgY29sb3I6IGdsb2JhbHMuJGdyYXktNjAwO1xufVxuXG4ubW9kYWwtZm9vdGVyIHtcbiAgYm9yZGVyLXRvcDogMDtcbn1cbiIsIiRmb250LWZhbWlseS1iYXNlOiBJbnRlciwgc2Fucy1zZXJpZjtcbiRoZWFkZXItaGVpZ2h0OiA0LjVyZW07XG4kZm9vdGVyLWhlaWdodDogNS41cmVtO1xuXG4kcHJpbWFyeS0yMDA6ICM5NkMwRTA7XG4kcHJpbWFyeS01MDA6ICMxQjc1QkI7XG4kcHJpbWFyeS02MDA6ICMxOTZBQUE7XG4kcHJpbWFyeS03MDA6ICMxMzUzODU7XG5cbiRncmF5LTUwOiAjRjlGQUZCO1xuJGdyYXktMTAwOiAjRjJGNEY3O1xuJGdyYXktMjAwOiAjRUFFQ0YwO1xuJGdyYXktMzAwOiAjRDBENUREO1xuJGdyYXktNjAwOiAjNDc1NDY3O1xuJGdyYXktNzAwOiAjMzQ0MDU0O1xuJGdyYXktODAwOiAjMUQyOTM5O1xuJGdyYXktOTAwOiAjMTAxODI4O1xuXG5cbiRsaW5rLWNvbG9yOiAkcHJpbWFyeS01MDAgIWRlZmF1bHQ7XG5cbkBtaXhpbiBoaWRlLXNjcm9sbGJhcnMge1xuICBzY3JvbGxiYXItd2lkdGg6IG5vbmU7XG4gIC1tcy1vdmVyZmxvdy1zdHlsZTogbm9uZTtcbiAgJjo6LXdlYmtpdC1zY3JvbGxiYXIge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cbn1cbiJdLCJzb3VyY2VSb290IjoiIn0= */"]
    });
  }
  return ModalComponent;
})();

/***/ }),

/***/ 6218:
/*!*************************************************************!*\
  !*** ./src/app/components/not-found/not-found.component.ts ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NotFoundComponent: () => (/* binding */ NotFoundComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _error_error_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../error/error.component */ 9426);


let NotFoundComponent = /*#__PURE__*/(() => {
  class NotFoundComponent {
    constructor() {}
    static #_ = this.ɵfac = function NotFoundComponent_Factory(t) {
      return new (t || NotFoundComponent)();
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: NotFoundComponent,
      selectors: [["theia-not-found"]],
      decls: 1,
      vars: 0,
      consts: [["description", "The page was not found", "error", "Not Found", "header", "404"]],
      template: function NotFoundComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "theia-error", 0);
        }
      },
      dependencies: [_error_error_component__WEBPACK_IMPORTED_MODULE_1__.ErrorComponent],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return NotFoundComponent;
})();

/***/ }),

/***/ 2649:
/*!***************************************************************!*\
  !*** ./src/app/components/pagination/pagination.component.ts ***!
  \***************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PaginationComponent: () => (/* binding */ PaginationComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ 6575);



const _c0 = function (a0, a1) {
  return {
    "active": a0,
    "disabled": a1
  };
};
function PaginationComponent_nav_0_ng_container_6_Template(rf, ctx) {
  if (rf & 1) {
    const _r4 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "a", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function PaginationComponent_nav_0_ng_container_6_Template_a_click_1_listener($event) {
      const restoredCtx = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r4);
      const page_r2 = restoredCtx.$implicit;
      const ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r3.handlePageClick($event, +page_r2));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const page_r2 = ctx.$implicit;
    const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction2"](2, _c0, page_r2 === ctx_r1.currentPage, page_r2 === "..."));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", page_r2, " ");
  }
}
const _c1 = function (a0) {
  return {
    "disabled": a0
  };
};
function PaginationComponent_nav_0_Template(rf, ctx) {
  if (rf & 1) {
    const _r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "nav", 1)(1, "button", 2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function PaginationComponent_nav_0_Template_button_click_1_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r6);
      const ctx_r5 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r5.handlePageClick($event, ctx_r5.currentPage - 1));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "svg", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](3, "path", 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](4, " Previous ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceHTML"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "div");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](6, PaginationComponent_nav_0_ng_container_6_Template, 3, 5, "ng-container", 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](7, "button", 2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function PaginationComponent_nav_0_Template_button_click_7_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r6);
      const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r7.handlePageClick($event, ctx_r7.currentPage + 1));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](8, " Next ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](9, "svg", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](10, "path", 6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](3, _c1, ctx_r0.currentPage === 1));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r0.pages);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](5, _c1, ctx_r0.currentPage === ctx_r0.Math.ceil(ctx_r0.totalItems / ctx_r0.itemsPerPage)));
  }
}
let PaginationComponent = /*#__PURE__*/(() => {
  class PaginationComponent {
    constructor() {
      this.totalItems = 0;
      this.currentPage = 1;
      this.itemsPerPage = 50;
      this.pageChange = new _angular_core__WEBPACK_IMPORTED_MODULE_0__.EventEmitter();
      this.itemsPerPageChange = new _angular_core__WEBPACK_IMPORTED_MODULE_0__.EventEmitter();
      this.pages = [];
      this.maxPages = 5;
      this.Math = Math;
    }
    ngOnInit() {
      this.setPages();
    }
    handlePageClick(event, page) {
      event.preventDefault();
      this.pageChange.emit(page);
      this.currentPage = page;
      this.setPages();
    }
    setPages() {
      const range = (lo, hi) => Array.from({
        length: hi - lo
      }, (_, i) => i + lo);
      const pagination = (count, page, total) => {
        const start = Math.max(1, Math.min(page - Math.floor((count - 3) / 2), total - count + 2));
        const end = Math.min(total, Math.max(page + Math.floor((count - 2) / 2), count - 1));
        return [...(start > 2 ? [1, "..."] : start > 1 ? [1] : []), ...range(start, end + 1), ...(end < total - 1 ? ["...", total] : end < total ? [total] : [])];
      };
      this.pages = pagination(this.maxPages, this.currentPage, Math.ceil(this.totalItems / this.itemsPerPage));
    }
    static #_ = this.ɵfac = function PaginationComponent_Factory(t) {
      return new (t || PaginationComponent)();
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: PaginationComponent,
      selectors: [["theia-pagination"]],
      inputs: {
        totalItems: "totalItems",
        currentPage: "currentPage",
        itemsPerPage: "itemsPerPage"
      },
      outputs: {
        pageChange: "pageChange",
        itemsPerPageChange: "itemsPerPageChange"
      },
      decls: 1,
      vars: 1,
      consts: [["aria-label", "", "class", "d-flex justify-content-between align-items-center px-4 pb-4", 4, "ngIf"], ["aria-label", "", 1, "d-flex", "justify-content-between", "align-items-center", "px-4", "pb-4"], [1, "btn", "btn-sm", "btn-outline-secondary", 3, "ngClass", "click"], ["xmlns", "http://www.w3.org/2000/svg", "width", "20", "height", "20", "viewBox", "0 0 20 20", "fill", "none"], ["d", "M15.8333 9.99984H4.16663M4.16663 9.99984L9.99996 15.8332M4.16663 9.99984L9.99996 4.1665", "stroke", "#344054", "stroke-width", "1.66667", "stroke-linecap", "round", "stroke-linejoin", "round"], [4, "ngFor", "ngForOf"], ["d", "M4.16669 9.99984H15.8334M15.8334 9.99984L10 4.1665M15.8334 9.99984L10 15.8332", "stroke", "#344054", "stroke-width", "1.66667", "stroke-linecap", "round", "stroke-linejoin", "round"], ["href", "#", 3, "ngClass", "click"]],
      template: function PaginationComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](0, PaginationComponent_nav_0_Template, 11, 7, "nav", 0);
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.totalItems !== 0 && ctx.Math.ceil(ctx.totalItems / ctx.itemsPerPage) > 1);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_1__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_1__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_1__.NgIf],
      styles: ["nav[_ngcontent-%COMP%]   div[_ngcontent-%COMP%] {\n  display: flex;\n}\nnav[_ngcontent-%COMP%]   div[_ngcontent-%COMP%]   a[_ngcontent-%COMP%] {\n  display: flex;\n  width: 2.5rem;\n  height: 2.5rem;\n  justify-content: center;\n  align-items: center;\n  border-radius: 8px;\n  font-weight: 500;\n  color: #1D2939;\n  text-decoration: none;\n}\nnav[_ngcontent-%COMP%]   div[_ngcontent-%COMP%]   a.active[_ngcontent-%COMP%] {\n  background-color: #F9FAFB;\n}\nnav[_ngcontent-%COMP%]   div[_ngcontent-%COMP%]   a.disabled[_ngcontent-%COMP%] {\n  pointer-events: none;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9wYWdpbmF0aW9uL3BhZ2luYXRpb24uY29tcG9uZW50LnNjc3MiLCJ3ZWJwYWNrOi8vLi9zcmMvX2dsb2JhbHMuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFHRTtFQUNFLGFBQUE7QUFGSjtBQUdJO0VBQ0UsYUFBQTtFQUNBLGFBQUE7RUFDQSxjQUFBO0VBQ0EsdUJBQUE7RUFDQSxtQkFBQTtFQUNBLGtCQUFBO0VBQ0EsZ0JBQUE7RUFDQSxjQ0VLO0VEREwscUJBQUE7QUFETjtBQUdNO0VBQ0UseUJDUkU7QURPVjtBQUlNO0VBQ0Usb0JBQUE7QUFGUiIsInNvdXJjZXNDb250ZW50IjpbIkB1c2UgXCIuLi8uLi8uLi9nbG9iYWxzXCI7XG5cbm5hdiB7XG4gIGRpdiB7XG4gICAgZGlzcGxheTogZmxleDtcbiAgICBhIHtcbiAgICAgIGRpc3BsYXk6IGZsZXg7XG4gICAgICB3aWR0aDogMi41cmVtO1xuICAgICAgaGVpZ2h0OiAyLjVyZW07XG4gICAgICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbiAgICAgIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gICAgICBib3JkZXItcmFkaXVzOiA4cHg7XG4gICAgICBmb250LXdlaWdodDogNTAwO1xuICAgICAgY29sb3I6IGdsb2JhbHMuJGdyYXktODAwO1xuICAgICAgdGV4dC1kZWNvcmF0aW9uOiBub25lO1xuXG4gICAgICAmLmFjdGl2ZSB7XG4gICAgICAgIGJhY2tncm91bmQtY29sb3I6IGdsb2JhbHMuJGdyYXktNTA7XG4gICAgICB9XG5cbiAgICAgICYuZGlzYWJsZWQge1xuICAgICAgICBwb2ludGVyLWV2ZW50czogbm9uZTtcbiAgICAgIH1cbiAgICB9XG4gIH1cbn1cbiIsIiRmb250LWZhbWlseS1iYXNlOiBJbnRlciwgc2Fucy1zZXJpZjtcbiRoZWFkZXItaGVpZ2h0OiA0LjVyZW07XG4kZm9vdGVyLWhlaWdodDogNS41cmVtO1xuXG4kcHJpbWFyeS0yMDA6ICM5NkMwRTA7XG4kcHJpbWFyeS01MDA6ICMxQjc1QkI7XG4kcHJpbWFyeS02MDA6ICMxOTZBQUE7XG4kcHJpbWFyeS03MDA6ICMxMzUzODU7XG5cbiRncmF5LTUwOiAjRjlGQUZCO1xuJGdyYXktMTAwOiAjRjJGNEY3O1xuJGdyYXktMjAwOiAjRUFFQ0YwO1xuJGdyYXktMzAwOiAjRDBENUREO1xuJGdyYXktNjAwOiAjNDc1NDY3O1xuJGdyYXktNzAwOiAjMzQ0MDU0O1xuJGdyYXktODAwOiAjMUQyOTM5O1xuJGdyYXktOTAwOiAjMTAxODI4O1xuXG5cbiRsaW5rLWNvbG9yOiAkcHJpbWFyeS01MDAgIWRlZmF1bHQ7XG5cbkBtaXhpbiBoaWRlLXNjcm9sbGJhcnMge1xuICBzY3JvbGxiYXItd2lkdGg6IG5vbmU7XG4gIC1tcy1vdmVyZmxvdy1zdHlsZTogbm9uZTtcbiAgJjo6LXdlYmtpdC1zY3JvbGxiYXIge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cbn1cbiJdLCJzb3VyY2VSb290IjoiIn0= */"]
    });
  }
  return PaginationComponent;
})();

/***/ }),

/***/ 7350:
/*!*******************************************************!*\
  !*** ./src/app/components/readme/readme.component.ts ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ReadmeComponent: () => (/* binding */ ReadmeComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_template_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../services/template.service */ 529);
/* harmony import */ var ngx_markdown__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ngx-markdown */ 1995);
/* harmony import */ var _layout_layout_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../layout/layout.component */ 2952);




let ReadmeComponent = /*#__PURE__*/(() => {
  class ReadmeComponent {
    constructor(templateService) {
      this.templateService = templateService;
      this.content = '';
    }
    ngOnInit() {
      this.content = this.templateService.getSectionByRoute('readme')?.description || '';
    }
    static #_ = this.ɵfac = function ReadmeComponent_Factory(t) {
      return new (t || ReadmeComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_template_service__WEBPACK_IMPORTED_MODULE_1__.TemplateService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: ReadmeComponent,
      selectors: [["theia-readme"]],
      decls: 4,
      vars: 1,
      consts: [[1, "card"], [1, "card-body"], ["markdown", "", 3, "data"]],
      template: function ReadmeComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "theia-layout")(1, "div", 0)(2, "div", 1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](3, "div", 2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("data", ctx.content);
        }
      },
      dependencies: [ngx_markdown__WEBPACK_IMPORTED_MODULE_2__.MarkdownComponent, _layout_layout_component__WEBPACK_IMPORTED_MODULE_3__.LayoutComponent],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return ReadmeComponent;
})();

/***/ }),

/***/ 7954:
/*!*********************************************************!*\
  !*** ./src/app/components/sidebar/sidebar.component.ts ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SidebarComponent: () => (/* binding */ SidebarComponent)
/* harmony export */ });
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../models/template */ 5339);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_template_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../services/template.service */ 529);
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ 7947);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ 8849);
/* harmony import */ var _services_environment_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/environment.service */ 1574);








function SidebarComponent_img_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "img", 17);
  }
}
function SidebarComponent_img_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "img", 18);
  }
}
function SidebarComponent_div_15_Template(rf, ctx) {
  if (rf & 1) {
    const _r5 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 19)(1, "a", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function SidebarComponent_div_15_Template_a_click_1_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r5);
      const ctx_r4 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r4.collapseAll($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](2, "i", 21);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
}
const _c0 = function (a1) {
  return ["/", a1];
};
const _c1 = function (a0) {
  return {
    "icon-active": a0
  };
};
function SidebarComponent_li_17_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "a", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](2, "img", 27, 28);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "span");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const _r11 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](3);
    const section_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("routerLink", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](5, _c0, section_r6.route));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("src", section_r6.icon, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsanitizeUrl"])("routerLink", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](7, _c0, section_r6.route))("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](9, _c1, _r11.isActive));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](section_r6.label);
  }
}
function SidebarComponent_li_17_ng_template_2__svg_svg_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "svg", 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "path", 32);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
function SidebarComponent_li_17_ng_template_2__svg_svg_5_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "svg", 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "path", 33);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
function SidebarComponent_li_17_ng_template_2_Template(rf, ctx) {
  if (rf & 1) {
    const _r17 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "a", 29);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function SidebarComponent_li_17_ng_template_2_Template_a_click_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r17);
      const section_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
      const ctx_r15 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r15.toggleSection($event, section_r6));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "img", 30);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "span");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, SidebarComponent_li_17_ng_template_2__svg_svg_4_Template, 2, 0, "svg", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](5, SidebarComponent_li_17_ng_template_2__svg_svg_5_Template, 2, 0, "svg", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const section_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    const ctx_r9 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵclassProp"]("active", ctx_r9.currentSection === section_r6.route);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("src", section_r6.icon, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsanitizeUrl"])("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](7, _c1, ctx_r9.currentSection === section_r6.route));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](section_r6.label);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !section_r6.open);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", section_r6.open);
  }
}
function SidebarComponent_li_17_ul_4_li_1_span_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "span", 39);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "i", 40);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
const _c2 = function (a0, a1, a2) {
  return [a0, a1, a2];
};
function SidebarComponent_li_17_ul_4_li_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "li", 36)(1, "a", 37);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, SidebarComponent_li_17_ul_4_li_1_span_3_Template, 2, 0, "span", 38);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const action_r20 = ctx.$implicit;
    const section_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2).$implicit;
    const ctx_r19 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("routerLink", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction3"](3, _c2, section_r6.static ? "" : "/action", section_r6.route, action_r20.id));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](action_r20.label);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r19.isHighlighted(action_r20.id));
  }
}
function SidebarComponent_li_17_ul_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "ul", 34);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, SidebarComponent_li_17_ul_4_li_1_Template, 4, 7, "li", 35);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const section_r6 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", section_r6 == null ? null : section_r6.actions);
  }
}
function SidebarComponent_li_17_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "li", 22);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, SidebarComponent_li_17_ng_container_1_Template, 6, 11, "ng-container", 23);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, SidebarComponent_li_17_ng_template_2_Template, 6, 9, "ng-template", null, 24, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplateRefExtractor"]);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, SidebarComponent_li_17_ul_4_Template, 2, 1, "ul", 25);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const section_r6 = ctx.$implicit;
    const _r8 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵreference"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", section_r6.static)("ngIfElse", _r8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", section_r6.open);
  }
}
const _c3 = function () {
  return ["/"];
};
const _c4 = function (a0) {
  return {
    collapsed: a0
  };
};
let SidebarComponent = /*#__PURE__*/(() => {
  class SidebarComponent {
    get filter() {
      return this.form.get('filter');
    }
    get sections() {
      return this.template$.getValue()?.sections?.filter(section => section.id !== 'setup');
    }
    constructor(templateService, router, activatedRoute, fb, env, document) {
      this.templateService = templateService;
      this.router = router;
      this.activatedRoute = activatedRoute;
      this.fb = fb;
      this.env = env;
      this.document = document;
      this.filteredSections = [];
      this.TheiaType = _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaType;
      this.currentSection = null;
      this.form = this.fb.group({
        filter: ''
      });
      this.collapsed = false;
      this.animating = false;
      this.hover = false;
      this.template$ = templateService.template$;
    }
    onMouseMove(event) {
      event.stopPropagation();
      const filter = this.document.querySelector('.filter-sidebar');
      if (!this.collapsed || filter && filter.contains(event.target)) {
        return;
      }
      this.hover = true;
    }
    onMouseLeave() {
      this.hover = false;
    }
    ngOnInit() {
      this.activatedRoute.paramMap.subscribe(params => {
        this.currentSection = params.get('route');
        if (this.currentSection) {
          const section = this.templateService.getSectionByRoute(this.currentSection);
          if (section) {
            section.open = true;
          }
        }
      });
      this.filter.valueChanges.subscribe(value => {
        const sections = JSON.parse(JSON.stringify(this.sections));
        this.filteredSections = !value.length ? sections : sections.filter(section => {
          const re = new RegExp(value, 'i');
          const filteredActions = section?.actions?.filter(action => re.test(action.label)) || [];
          if (re.test(section.label) && !filteredActions.length) {
            return true;
          } else if (filteredActions.length) {
            section.open = true;
            section.actions = filteredActions;
            return true;
          }
          return false;
        }) || [];
      });
      this.updateFilteredSections();
      this.env.highlightedActions$.subscribe(this.updateFilteredSections.bind(this));
    }
    updateFilteredSections() {
      this.filteredSections = this.sections?.map(section => {
        if ((section.actions || []).map(v => v.id).some(this.isHighlighted.bind(this))) {
          section.open = true;
        }
        return section;
      }) || [];
    }
    toggleSection(event, section) {
      event.preventDefault();
      section.open = !section.open;
    }
    toggleSidebar(event) {
      event.preventDefault();
      this.animating = true;
      this.collapsed = !this.collapsed;
      setTimeout(() => this.animating = false, 250);
    }
    isHighlighted(id) {
      return this.env.highlightedActions$.value.includes(id);
    }
    collapseAll(event) {
      event.preventDefault();
      this.filteredSections.forEach(section => {
        section.open = false;
      });
    }
    hasSectionsOpen() {
      return this.filteredSections.some(section => section.open);
    }
    static #_ = this.ɵfac = function SidebarComponent_Factory(t) {
      return new (t || SidebarComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_template_service__WEBPACK_IMPORTED_MODULE_2__.TemplateService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_router__WEBPACK_IMPORTED_MODULE_3__.Router), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_router__WEBPACK_IMPORTED_MODULE_3__.ActivatedRoute), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_forms__WEBPACK_IMPORTED_MODULE_4__.UntypedFormBuilder), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_environment_service__WEBPACK_IMPORTED_MODULE_5__.EnvironmentService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_common__WEBPACK_IMPORTED_MODULE_6__.DOCUMENT));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: SidebarComponent,
      selectors: [["theia-sidebar"]],
      hostVars: 6,
      hostBindings: function SidebarComponent_HostBindings(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("mousemove", function SidebarComponent_mousemove_HostBindingHandler($event) {
            return ctx.onMouseMove($event);
          })("mouseleave", function SidebarComponent_mouseleave_HostBindingHandler() {
            return ctx.onMouseLeave();
          });
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵclassProp"]("collapsed", ctx.collapsed)("animating", ctx.animating)("hover", ctx.hover);
        }
      },
      decls: 18,
      vars: 11,
      consts: [[1, "sidebar"], [1, "logo", "w-100"], [1, "navbar-brand", 3, "routerLink"], ["alt", "RapidCloud", "ngSrc", "assets/img/logo-transparent.png", "height", "24", "width", "142", 4, "ngIf"], ["alt", "RapidCloud", "ngSrc", "assets/img/logo-sm.png", "height", "32", "width", "33", 4, "ngIf"], [1, "py-1", "filter-sidebar"], [1, "", 3, "formGroup"], [1, "search-input"], ["xmlns", "http://www.w3.org/2000/svg", "width", "20", "height", "20", "viewBox", "0 0 20 20", "fill", "none"], ["d", "M17.5 17.5L14.5834 14.5833M16.6667 9.58333C16.6667 13.4954 13.4954 16.6667 9.58333 16.6667C5.67132 16.6667 2.5 13.4954 2.5 9.58333C2.5 5.67132 5.67132 2.5 9.58333 2.5C13.4954 2.5 16.6667 5.67132 16.6667 9.58333Z", "stroke", "#667085", "stroke-width", "1.66667", "stroke-linecap", "round", "stroke-linejoin", "round"], ["placeholder", "Search...", "type", "search", 1, "form-control", "filter", 3, "formControl"], ["href", "", 1, "fs-5", "text-body", "collapse-button", 3, "click"], ["d", "M15 14.1663L10.8333 9.99967L15 5.83301M9.16667 14.1663L5 9.99967L9.16667 5.83301", "stroke", "#667085", "stroke-width", "1.66667", "stroke-linecap", "round", "stroke-linejoin", "round"], [1, "expanded-menu", 3, "ngClass"], ["class", "collapse-all fs-5", 4, "ngIf"], [1, "list-unstyled", "text-nowrap"], ["class", "nav-item", 4, "ngFor", "ngForOf"], ["alt", "RapidCloud", "ngSrc", "assets/img/logo-transparent.png", "height", "24", "width", "142"], ["alt", "RapidCloud", "ngSrc", "assets/img/logo-sm.png", "height", "32", "width", "33"], [1, "collapse-all", "fs-5"], ["href", "", 3, "click"], ["title", "Collapse all", 1, "bi", "bi-arrows-collapse"], [1, "nav-item"], [4, "ngIf", "ngIfElse"], ["dynamicSection", ""], ["class", "list-unstyled", 4, "ngIf"], ["routerLinkActive", "active", 1, "section", "d-inline-flex", "align-items-center", "justify-content-between", "rounded", 3, "routerLink"], ["alt", "", "routerLinkActive", "", 1, "section-icon", 3, "src", "routerLink", "ngClass"], ["rla", "routerLinkActive"], ["href", "#", 1, "section", "d-inline-flex", "align-items-center", "justify-content-between", "rounded", 3, "click"], ["alt", "", 1, "section-icon", 3, "src", "ngClass"], ["xmlns", "http://www.w3.org/2000/svg", "width", "20", "height", "20", "viewBox", "0 0 20 20", "fill", "none", 4, "ngIf"], ["d", "M5 7.5L10 12.5L15 7.5", "stroke", "#667085", "stroke-width", "1.66667", "stroke-linecap", "round", "stroke-linejoin", "round"], ["d", "M15 12.5L10 7.5L5 12.5", "stroke", "#667085", "stroke-width", "2", "stroke-linecap", "round", "stroke-linejoin", "round"], [1, "list-unstyled"], ["class", "d-flex align-items-center", 4, "ngFor", "ngForOf"], [1, "d-flex", "align-items-center"], ["routerLinkActive", "active", 1, "action", "d-flex", "align-items-center", 3, "routerLink"], ["class", "text-primary highlight", 4, "ngIf"], [1, "text-primary", "highlight"], [1, "bi", "bi-circle-fill"]],
      template: function SidebarComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 0)(1, "div", 1)(2, "a", 2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, SidebarComponent_img_3_Template, 1, 0, "img", 3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, SidebarComponent_img_4_Template, 1, 0, "img", 4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](5, "div", 5)(6, "form", 6)(7, "div", 7);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](8, "svg", 8);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](9, "path", 9);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceHTML"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](10, "input", 10);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](11, "a", 11);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function SidebarComponent_Template_a_click_11_listener($event) {
            return ctx.toggleSidebar($event);
          });
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](12, "svg", 8);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](13, "path", 12);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceHTML"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](14, "aside", 13);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](15, SidebarComponent_div_15_Template, 3, 0, "div", 14);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](16, "ul", 15);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](17, SidebarComponent_li_17_Template, 5, 3, "li", 16);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("routerLink", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction0"](8, _c3));
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !ctx.collapsed);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.collapsed);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formGroup", ctx.form);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formControl", ctx.filter);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](9, _c4, ctx.collapsed));
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.hasSectionsOpen());
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx.filteredSections);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_6__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_6__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_6__.NgIf, _angular_router__WEBPACK_IMPORTED_MODULE_3__.RouterLink, _angular_router__WEBPACK_IMPORTED_MODULE_3__.RouterLinkActive, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ɵNgNoValidate"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__.DefaultValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_4__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_4__.NgControlStatusGroup, _angular_forms__WEBPACK_IMPORTED_MODULE_4__.FormControlDirective, _angular_forms__WEBPACK_IMPORTED_MODULE_4__.FormGroupDirective, _angular_common__WEBPACK_IMPORTED_MODULE_6__.NgOptimizedImage],
      styles: ["a[_ngcontent-%COMP%]:hover {\n  color: var(--bs-primary) !important;\n}\n\n[_nghost-%COMP%] {\n  transition: 0.25s ease-in;\n  position: relative;\n  height: calc(100vh - 5.5rem);\n  padding-right: 0;\n  padding-left: 0;\n  max-width: 20rem;\n  background-color: white;\n  overflow: hidden;\n  box-shadow: 0 8px 8px -4px rgba(16, 24, 40, 0.03), 0px 20px 24px -4px rgba(16, 24, 40, 0.08);\n}\n.hover[_nghost-%COMP%]   .sidebar[_ngcontent-%COMP%] {\n  position: fixed;\n  width: 20rem;\n  overflow-x: hidden;\n  z-index: 1031;\n  background-color: white;\n  height: calc(100vh - 5.5rem);\n  transition: width 0.25s ease-out;\n}\n[_nghost-%COMP%]   .sidebar[_ngcontent-%COMP%] {\n  height: 100%;\n  overflow: hidden;\n}\n[_nghost-%COMP%]   .filter-sidebar[_ngcontent-%COMP%] {\n  padding-right: calc(var(--bs-gutter-x) * 0.5);\n  padding-left: calc(var(--bs-gutter-x) * 0.5);\n  background-color: white;\n  position: sticky;\n  z-index: 5;\n}\n[_nghost-%COMP%]   .highlight[_ngcontent-%COMP%] {\n  font-size: 0.5rem;\n}\n[_nghost-%COMP%]   .filter[_ngcontent-%COMP%] {\n  width: 90%;\n}\n[_nghost-%COMP%]   aside[_ngcontent-%COMP%] {\n  padding-top: 0.5rem;\n  padding-right: 1rem;\n  padding-left: 1rem;\n  overflow: auto;\n  max-width: 100%;\n  transition: max-width 0.25s ease-in;\n  height: calc(100% - 3.25rem);\n}\n[_nghost-%COMP%]   aside[_ngcontent-%COMP%]   ul[_ngcontent-%COMP%]   li[_ngcontent-%COMP%] {\n  min-height: 2.5rem;\n  padding-bottom: 0.25rem;\n}\n[_nghost-%COMP%]   aside[_ngcontent-%COMP%]   ul[_ngcontent-%COMP%]   li[_ngcontent-%COMP%]   ul[_ngcontent-%COMP%] {\n  max-height: 100%;\n  padding-top: 0.5rem;\n  transition: max-height 0.25s ease-in;\n}\n[_nghost-%COMP%]   aside.collapsed-menu[_ngcontent-%COMP%] {\n  position: absolute;\n  left: 20.67rem;\n  top: 3.5rem;\n}\n[_nghost-%COMP%]   aside[_ngcontent-%COMP%]   a[_ngcontent-%COMP%] {\n  text-decoration: none;\n  border-radius: 6px;\n  min-height: 2.5rem;\n  padding: 0.25rem 0.5rem;\n  color: #344054;\n  font-weight: 600;\n}\n[_nghost-%COMP%]   aside[_ngcontent-%COMP%]   a.section[_ngcontent-%COMP%] {\n  width: 100%;\n  background-color: transparent;\n  border: 0;\n  cursor: pointer;\n}\n[_nghost-%COMP%]   aside[_ngcontent-%COMP%]   a.section.active[_ngcontent-%COMP%] {\n  color: #1B75BB !important;\n  background-color: #F2F4F7;\n}\n[_nghost-%COMP%]   aside[_ngcontent-%COMP%]   a.section.active[_ngcontent-%COMP%]:hover {\n  color: #101828 !important;\n  background-color: #F2F4F7;\n}\n[_nghost-%COMP%]   aside[_ngcontent-%COMP%]   a.section.active[_ngcontent-%COMP%]:hover   .section-icon[_ngcontent-%COMP%] {\n  filter: initial;\n}\n[_nghost-%COMP%]   aside[_ngcontent-%COMP%]   a.section[_ngcontent-%COMP%]:hover {\n  color: #101828 !important;\n  background-color: #F9FAFB;\n}\n[_nghost-%COMP%]   aside[_ngcontent-%COMP%]   a.action[_ngcontent-%COMP%] {\n  padding-left: 2.75rem;\n  cursor: pointer;\n  width: 100%;\n  color: #344054;\n}\n[_nghost-%COMP%]   aside[_ngcontent-%COMP%]   a.action.active[_ngcontent-%COMP%] {\n  color: white;\n  background-color: #196AAA;\n}\n[_nghost-%COMP%]   aside[_ngcontent-%COMP%]   a.action.active[_ngcontent-%COMP%]:hover {\n  color: white !important;\n  background-color: #196AAA;\n}\n[_nghost-%COMP%]   aside[_ngcontent-%COMP%]   a.action[_ngcontent-%COMP%]:hover {\n  color: #101828 !important;\n  background-color: #F9FAFB;\n}\n[_nghost-%COMP%]   .collapse-button[_ngcontent-%COMP%] {\n  position: absolute;\n  right: 0.25rem;\n  top: 0.75rem;\n  display: block;\n  transform: rotate(0deg);\n  transition: 0.5s ease-in;\n  z-index: 10;\n  height: 1.25rem;\n  line-height: 1.25rem;\n}\n[_nghost-%COMP%]   .collapse-all[_ngcontent-%COMP%] {\n  position: sticky;\n  top: 0;\n}\n[_nghost-%COMP%]   .collapse-all[_ngcontent-%COMP%]   a[_ngcontent-%COMP%] {\n  position: absolute;\n  right: 0;\n}\n[_nghost-%COMP%]   .collapse-all[_ngcontent-%COMP%]   a[_ngcontent-%COMP%]   i[_ngcontent-%COMP%] {\n  background-color: transparent;\n}\n\n.collapsed[_nghost-%COMP%] {\n  width: 4.5rem;\n  transition: 0.1s ease-out;\n  white-space: nowrap;\n  scrollbar-width: none;\n  -ms-overflow-style: none;\n}\n.collapsed[_nghost-%COMP%]::-webkit-scrollbar {\n  display: none;\n}\n.collapsed.hover[_nghost-%COMP%]   .sidebar[_ngcontent-%COMP%] {\n  position: fixed;\n  width: 20rem;\n  z-index: 1031;\n  overflow: hidden;\n  background-color: white;\n  border-right: 1px solid #dee2e6 !important;\n  border-bottom: 1px solid #dee2e6 !important;\n  height: calc(100vh - 5.5rem);\n  transition: width 0.25s ease-out;\n}\n.collapsed[_nghost-%COMP%]:not(.hover)   .filter-sidebar[_ngcontent-%COMP%]   a[_ngcontent-%COMP%] {\n  right: 1.5rem;\n}\n.collapsed[_nghost-%COMP%]:not(.hover)   aside[_ngcontent-%COMP%] {\n  min-width: 4.5rem;\n  max-width: 4.5rem;\n  transition: max-width 0.25s ease-out;\n  overflow: hidden;\n}\n.collapsed[_nghost-%COMP%]:not(.hover)   aside[_ngcontent-%COMP%]   ul[_ngcontent-%COMP%]   li[_ngcontent-%COMP%]   a[_ngcontent-%COMP%]    > span[_ngcontent-%COMP%], .collapsed[_nghost-%COMP%]:not(.hover)   aside[_ngcontent-%COMP%]   ul[_ngcontent-%COMP%]   li[_ngcontent-%COMP%]   a[_ngcontent-%COMP%]    > svg[_ngcontent-%COMP%] {\n  display: none;\n}\n.collapsed[_nghost-%COMP%]:not(.hover)   aside[_ngcontent-%COMP%]   ul[_ngcontent-%COMP%]   li[_ngcontent-%COMP%]   ul[_ngcontent-%COMP%] {\n  display: none;\n}\n.collapsed[_nghost-%COMP%]:not(.hover)   .collapse-all[_ngcontent-%COMP%] {\n  display: none;\n}\n.collapsed[_nghost-%COMP%]:not(.hover)   .filter[_ngcontent-%COMP%], .collapsed[_nghost-%COMP%]:not(.hover)   .search-input[_ngcontent-%COMP%]   svg[_ngcontent-%COMP%] {\n  transform: translateX(-20.67rem);\n  transition: 0.25s ease-out;\n}\n.collapsed[_nghost-%COMP%]   .collapse-button[_ngcontent-%COMP%] {\n  transform: rotate(-180deg);\n  transition: 0.5s ease-out;\n}\n\n.animating[_nghost-%COMP%] {\n  scrollbar-width: none;\n  -ms-overflow-style: none;\n}\n.animating[_nghost-%COMP%]::-webkit-scrollbar {\n  display: none;\n}\n.animating[_nghost-%COMP%]   aside[_ngcontent-%COMP%] {\n  scrollbar-width: none;\n  -ms-overflow-style: none;\n}\n.animating[_nghost-%COMP%]   aside[_ngcontent-%COMP%]::-webkit-scrollbar {\n  display: none;\n}\n\n.badge[_ngcontent-%COMP%] {\n  width: 3rem;\n}\n\n.nav-item[_ngcontent-%COMP%]   .section-icon[_ngcontent-%COMP%] {\n  width: 1.5rem;\n  height: 1.5rem;\n}\n.nav-item[_ngcontent-%COMP%]   .section-icon.icon-active[_ngcontent-%COMP%] {\n  filter: invert(28%) sepia(83%) saturate(2164%) hue-rotate(207deg) brightness(98%) contrast(103%);\n}\n.nav-item[_ngcontent-%COMP%]   span[_ngcontent-%COMP%] {\n  display: block;\n  flex-grow: 2;\n  padding-left: 0.75rem;\n  padding-right: 0.75rem;\n}\n\n.search-input[_ngcontent-%COMP%] {\n  position: relative;\n}\n.search-input[_ngcontent-%COMP%]   svg[_ngcontent-%COMP%] {\n  position: absolute;\n  pointer-events: none;\n  left: 0.75rem;\n  top: 0.75rem;\n}\n.search-input[_ngcontent-%COMP%]   input[_ngcontent-%COMP%] {\n  padding-left: 2.75rem;\n  height: 2.75rem;\n}\n\n.logo[_ngcontent-%COMP%] {\n  height: 4.5rem;\n  display: flex;\n  align-items: center;\n  padding-left: 1rem;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9zaWRlYmFyL3NpZGViYXIuY29tcG9uZW50LnNjc3MiLCJ3ZWJwYWNrOi8vLi9zcmMvX2dsb2JhbHMuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFLQTtFQUNFLG1DQUFBO0FBSkY7O0FBT0E7RUFDRSx5QkFBQTtFQUNBLGtCQUFBO0VBQ0EsNEJBQUE7RUFDQSxnQkFBQTtFQUNBLGVBQUE7RUFDQSxnQkFiZTtFQWNmLHVCQUFBO0VBQ0EsZ0JBQUE7RUFDQSw0RkFBQTtBQUpGO0FBT0k7RUFDRSxlQUFBO0VBQ0EsWUFyQlc7RUFzQlgsa0JBQUE7RUFDQSxhQUFBO0VBQ0EsdUJBQUE7RUFDQSw0QkFBQTtFQUNBLGdDQUFBO0FBTE47QUFTRTtFQUNFLFlBQUE7RUFDQSxnQkFBQTtBQVBKO0FBVUU7RUFDRSw2Q0FBQTtFQUNBLDRDQUFBO0VBQ0EsdUJBQUE7RUFDQSxnQkFBQTtFQUNBLFVBQUE7QUFSSjtBQVdFO0VBQ0UsaUJBQUE7QUFUSjtBQVlFO0VBQ0UsVUFBQTtBQVZKO0FBYUU7RUFDRSxtQkFBQTtFQUNBLG1CQUFBO0VBQ0Esa0JBQUE7RUFDQSxjQUFBO0VBRUEsZUFBQTtFQUNBLG1DQUFBO0VBR0EsNEJBQUE7QUFkSjtBQWdCSTtFQUNFLGtCQUFBO0VBQ0EsdUJBQUE7QUFkTjtBQWVNO0VBQ0UsZ0JBQUE7RUFDQSxtQkFBQTtFQUNBLG9DQUFBO0FBYlI7QUFpQkk7RUFDRSxrQkFBQTtFQUNBLGNBQUE7RUFDQSxXQUFBO0FBZk47QUFrQkk7RUFDRSxxQkFBQTtFQUNBLGtCQUFBO0VBQ0Esa0JBQUE7RUFDQSx1QkFBQTtFQUNBLGNDeEVLO0VEeUVMLGdCQUFBO0FBaEJOO0FBa0JNO0VBQ0UsV0FBQTtFQUNBLDZCQUFBO0VBQ0EsU0FBQTtFQUNBLGVBQUE7QUFoQlI7QUFrQlE7RUFDRSx5QkFBQTtFQUNBLHlCQ3ZGQztBRHVFWDtBQWtCVTtFQUNFLHlCQUFBO0VBQ0EseUJDM0ZEO0FEMkVYO0FBa0JZO0VBQ0UsZUFBQTtBQWhCZDtBQXNCUTtFQUNFLHlCQUFBO0VBQ0EseUJDdkdBO0FEbUZWO0FBd0JNO0VBQ0UscUJBQUE7RUFDQSxlQUFBO0VBQ0EsV0FBQTtFQUNBLGNDMUdHO0FEb0ZYO0FBd0JRO0VBQ0UsWUFBQTtFQUNBLHlCQ3RISTtBRGdHZDtBQXdCVTtFQUNFLHVCQUFBO0VBQ0EseUJDMUhFO0FEb0dkO0FBMEJRO0VBQ0UseUJBQUE7RUFDQSx5QkM3SEE7QURxR1Y7QUE4QkU7RUFDRSxrQkFBQTtFQUNBLGNBQUE7RUFDQSxZQUFBO0VBQ0EsY0FBQTtFQUNBLHVCQUFBO0VBQ0Esd0JBQUE7RUFDQSxXQUFBO0VBQ0EsZUFBQTtFQUNBLG9CQUFBO0FBNUJKO0FBbUNFO0VBQ0UsZ0JBQUE7RUFDQSxNQUFBO0FBakNKO0FBbUNJO0VBQ0Usa0JBQUE7RUFDQSxRQUFBO0FBakNOO0FBbUNNO0VBQ0UsNkJBQUE7QUFqQ1I7O0FBdUNBO0VBQ0UsYUF6S2dCO0VBMEtoQix5QkFBQTtFQUNBLG1CQUFBO0VDeEpBLHFCQUFBO0VBQ0Esd0JBQUE7QURxSEY7QUNwSEU7RUFDRSxhQUFBO0FEc0hKO0FBbUNJO0VBQ0UsZUFBQTtFQUNBLFlBbExXO0VBbUxYLGFBQUE7RUFDQSxnQkFBQTtFQUNBLHVCQUFBO0VBQ0EsMENBQUE7RUFDQSwyQ0FBQTtFQUNBLDRCQUFBO0VBQ0EsZ0NBQUE7QUFqQ047QUF1Q007RUFDRSxhQUFBO0FBckNSO0FBd0NJO0VBQ0UsaUJBbk1ZO0VBb01aLGlCQXBNWTtFQXFNWixvQ0FBQTtFQUNBLGdCQUFBO0FBdENOO0FBeUNRO0VBQ0UsYUFBQTtBQXZDVjtBQXlDUTtFQUNFLGFBQUE7QUF2Q1Y7QUE0Q0k7RUFDRSxhQUFBO0FBMUNOO0FBNkNJO0VBQ0UsZ0NBQUE7RUFDQSwwQkFBQTtBQTNDTjtBQStDRTtFQUNFLDBCQUFBO0VBQ0EseUJBQUE7QUE3Q0o7O0FBaURBO0VDL01FLHFCQUFBO0VBQ0Esd0JBQUE7QURrS0Y7QUNqS0U7RUFDRSxhQUFBO0FEbUtKO0FBNENFO0VDbE5BLHFCQUFBO0VBQ0Esd0JBQUE7QUR5S0Y7QUN4S0U7RUFDRSxhQUFBO0FEMEtKOztBQTBDQTtFQUNFLFdBQUE7QUF2Q0Y7O0FBMkNFO0VBQ0UsYUFBQTtFQUNBLGNBQUE7QUF4Q0o7QUF5Q0k7RUFDRSxnR0FBQTtBQXZDTjtBQTBDRTtFQUNFLGNBQUE7RUFDQSxZQUFBO0VBQ0EscUJBQUE7RUFDQSxzQkFBQTtBQXhDSjs7QUE0Q0E7RUFDRSxrQkFBQTtBQXpDRjtBQTJDRTtFQUNFLGtCQUFBO0VBQ0Esb0JBQUE7RUFDQSxhQUFBO0VBQ0EsWUFBQTtBQXpDSjtBQTRDRTtFQUNFLHFCQUFBO0VBQ0EsZUFBQTtBQTFDSjs7QUE4Q0E7RUFDRSxjQ2pSYztFRGtSZCxhQUFBO0VBQ0EsbUJBQUE7RUFDQSxrQkFBQTtBQTNDRiIsInNvdXJjZXNDb250ZW50IjpbIkB1c2UgXCIuLi8uLi8uLi9nbG9iYWxzXCI7XG5cbiRleHBhbmRlZC13aWR0aDogMjByZW07XG4kY29sbGFwc2VkLXdpZHRoOiA0LjVyZW07XG5cbmE6aG92ZXIge1xuICBjb2xvcjogdmFyKC0tYnMtcHJpbWFyeSkgIWltcG9ydGFudDtcbn1cblxuOmhvc3Qge1xuICB0cmFuc2l0aW9uOiAuMjVzIGVhc2UtaW47XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgaGVpZ2h0OiBjYWxjKDEwMHZoIC0gI3tnbG9iYWxzLiRmb290ZXItaGVpZ2h0fSk7XG4gIHBhZGRpbmctcmlnaHQ6IDA7XG4gIHBhZGRpbmctbGVmdDogMDtcbiAgbWF4LXdpZHRoOiAkZXhwYW5kZWQtd2lkdGg7XG4gIGJhY2tncm91bmQtY29sb3I6IHdoaXRlO1xuICBvdmVyZmxvdzogaGlkZGVuO1xuICBib3gtc2hhZG93OiAwIDhweCA4cHggLTRweCByZ2JhKDE2LCAyNCwgNDAsIDAuMDMpLCAwcHggMjBweCAyNHB4IC00cHggcmdiYSgxNiwgMjQsIDQwLCAwLjA4KTtcblxuICAmLmhvdmVyIHtcbiAgICAuc2lkZWJhciB7XG4gICAgICBwb3NpdGlvbjogZml4ZWQ7XG4gICAgICB3aWR0aDogJGV4cGFuZGVkLXdpZHRoO1xuICAgICAgb3ZlcmZsb3cteDogaGlkZGVuO1xuICAgICAgei1pbmRleDogMTAzMTtcbiAgICAgIGJhY2tncm91bmQtY29sb3I6IHdoaXRlO1xuICAgICAgaGVpZ2h0OiBjYWxjKDEwMHZoIC0gI3tnbG9iYWxzLiRmb290ZXItaGVpZ2h0fSk7XG4gICAgICB0cmFuc2l0aW9uOiB3aWR0aCAuMjVzIGVhc2Utb3V0O1xuICAgIH1cbiAgfVxuXG4gIC5zaWRlYmFyIHtcbiAgICBoZWlnaHQ6IDEwMCU7XG4gICAgb3ZlcmZsb3c6IGhpZGRlbjtcbiAgfVxuXG4gIC5maWx0ZXItc2lkZWJhciB7XG4gICAgcGFkZGluZy1yaWdodDogY2FsYyh2YXIoLS1icy1ndXR0ZXIteCkgKiAuNSk7XG4gICAgcGFkZGluZy1sZWZ0OiBjYWxjKHZhcigtLWJzLWd1dHRlci14KSAqIC41KTtcbiAgICBiYWNrZ3JvdW5kLWNvbG9yOiB3aGl0ZTtcbiAgICBwb3NpdGlvbjogc3RpY2t5O1xuICAgIHotaW5kZXg6IDU7XG4gIH1cblxuICAuaGlnaGxpZ2h0IHtcbiAgICBmb250LXNpemU6IC41cmVtO1xuICB9XG5cbiAgLmZpbHRlciB7XG4gICAgd2lkdGg6IDkwJTtcbiAgfVxuXG4gIGFzaWRlIHtcbiAgICBwYWRkaW5nLXRvcDogLjVyZW07XG4gICAgcGFkZGluZy1yaWdodDogMXJlbTtcbiAgICBwYWRkaW5nLWxlZnQ6IDFyZW07XG4gICAgb3ZlcmZsb3c6IGF1dG87XG5cbiAgICBtYXgtd2lkdGg6IDEwMCU7XG4gICAgdHJhbnNpdGlvbjogbWF4LXdpZHRoIC4yNXMgZWFzZS1pbjtcblxuXG4gICAgaGVpZ2h0OiBjYWxjKDEwMCUgLSAzLjI1cmVtKTtcblxuICAgIHVsIGxpIHtcbiAgICAgIG1pbi1oZWlnaHQ6IDIuNXJlbTtcbiAgICAgIHBhZGRpbmctYm90dG9tOiAuMjVyZW07XG4gICAgICB1bCB7XG4gICAgICAgIG1heC1oZWlnaHQ6IDEwMCU7XG4gICAgICAgIHBhZGRpbmctdG9wOiAuNXJlbTtcbiAgICAgICAgdHJhbnNpdGlvbjogbWF4LWhlaWdodCAuMjVzIGVhc2UtaW47XG4gICAgICB9XG4gICAgfVxuXG4gICAgJi5jb2xsYXBzZWQtbWVudSB7XG4gICAgICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gICAgICBsZWZ0OiAyMC42N3JlbTtcbiAgICAgIHRvcDogMy41cmVtO1xuICAgIH1cblxuICAgIGEge1xuICAgICAgdGV4dC1kZWNvcmF0aW9uOiBub25lO1xuICAgICAgYm9yZGVyLXJhZGl1czogNnB4O1xuICAgICAgbWluLWhlaWdodDogMi41cmVtO1xuICAgICAgcGFkZGluZzogLjI1cmVtIC41cmVtO1xuICAgICAgY29sb3I6IGdsb2JhbHMuJGdyYXktNzAwO1xuICAgICAgZm9udC13ZWlnaHQ6IDYwMDtcblxuICAgICAgJi5zZWN0aW9uIHtcbiAgICAgICAgd2lkdGg6IDEwMCU7XG4gICAgICAgIGJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50O1xuICAgICAgICBib3JkZXI6IDA7XG4gICAgICAgIGN1cnNvcjogcG9pbnRlcjtcblxuICAgICAgICAmLmFjdGl2ZSB7XG4gICAgICAgICAgY29sb3I6IGdsb2JhbHMuJHByaW1hcnktNTAwICFpbXBvcnRhbnQ7XG4gICAgICAgICAgYmFja2dyb3VuZC1jb2xvcjogZ2xvYmFscy4kZ3JheS0xMDA7XG5cbiAgICAgICAgICAmOmhvdmVyIHtcbiAgICAgICAgICAgIGNvbG9yOiBnbG9iYWxzLiRncmF5LTkwMCAhaW1wb3J0YW50O1xuICAgICAgICAgICAgYmFja2dyb3VuZC1jb2xvcjogZ2xvYmFscy4kZ3JheS0xMDA7XG5cbiAgICAgICAgICAgIC5zZWN0aW9uLWljb24ge1xuICAgICAgICAgICAgICBmaWx0ZXI6IGluaXRpYWw7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfVxuXG4gICAgICAgIH1cblxuICAgICAgICAmOmhvdmVyIHtcbiAgICAgICAgICBjb2xvcjogZ2xvYmFscy4kZ3JheS05MDAgIWltcG9ydGFudDtcbiAgICAgICAgICBiYWNrZ3JvdW5kLWNvbG9yOiBnbG9iYWxzLiRncmF5LTUwO1xuICAgICAgICB9XG4gICAgICB9XG5cbiAgICAgICYuYWN0aW9uIHtcbiAgICAgICAgcGFkZGluZy1sZWZ0OiAyLjc1cmVtO1xuICAgICAgICBjdXJzb3I6IHBvaW50ZXI7XG4gICAgICAgIHdpZHRoOiAxMDAlO1xuICAgICAgICBjb2xvcjogZ2xvYmFscy4kZ3JheS03MDA7XG5cbiAgICAgICAgJi5hY3RpdmUge1xuICAgICAgICAgIGNvbG9yOiB3aGl0ZTtcbiAgICAgICAgICBiYWNrZ3JvdW5kLWNvbG9yOiBnbG9iYWxzLiRwcmltYXJ5LTYwMDtcblxuICAgICAgICAgICY6aG92ZXIge1xuICAgICAgICAgICAgY29sb3I6IHdoaXRlICFpbXBvcnRhbnQ7XG4gICAgICAgICAgICBiYWNrZ3JvdW5kLWNvbG9yOiBnbG9iYWxzLiRwcmltYXJ5LTYwMDtcbiAgICAgICAgICB9XG4gICAgICAgIH1cblxuICAgICAgICAmOmhvdmVyIHtcbiAgICAgICAgICBjb2xvcjogZ2xvYmFscy4kZ3JheS05MDAgIWltcG9ydGFudDtcbiAgICAgICAgICBiYWNrZ3JvdW5kLWNvbG9yOiBnbG9iYWxzLiRncmF5LTUwO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICB9XG5cbiAgLmNvbGxhcHNlLWJ1dHRvbiB7XG4gICAgcG9zaXRpb246IGFic29sdXRlO1xuICAgIHJpZ2h0OiAuMjVyZW07XG4gICAgdG9wOiAwLjc1cmVtO1xuICAgIGRpc3BsYXk6IGJsb2NrO1xuICAgIHRyYW5zZm9ybTogcm90YXRlKDBkZWcpO1xuICAgIHRyYW5zaXRpb246IC41cyBlYXNlLWluO1xuICAgIHotaW5kZXg6IDEwO1xuICAgIGhlaWdodDogMS4yNXJlbTtcbiAgICBsaW5lLWhlaWdodDogMS4yNXJlbTtcblxuICAgICY6aG92ZXIge1xuXG4gICAgfVxuICB9XG5cbiAgLmNvbGxhcHNlLWFsbCB7XG4gICAgcG9zaXRpb246IHN0aWNreTtcbiAgICB0b3A6IDA7XG5cbiAgICBhIHtcbiAgICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgICAgIHJpZ2h0OiAwO1xuXG4gICAgICBpIHtcbiAgICAgICAgYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7XG4gICAgICB9XG4gICAgfVxuICB9XG59XG5cbjpob3N0KC5jb2xsYXBzZWQpIHtcbiAgd2lkdGg6ICRjb2xsYXBzZWQtd2lkdGg7XG4gIHRyYW5zaXRpb246IC4xcyBlYXNlLW91dDtcbiAgd2hpdGUtc3BhY2U6IG5vd3JhcDtcbiAgQGluY2x1ZGUgZ2xvYmFscy5oaWRlLXNjcm9sbGJhcnM7XG5cbiAgJi5ob3ZlciB7XG4gICAgLnNpZGViYXIge1xuICAgICAgcG9zaXRpb246IGZpeGVkO1xuICAgICAgd2lkdGg6ICRleHBhbmRlZC13aWR0aDtcbiAgICAgIHotaW5kZXg6IDEwMzE7XG4gICAgICBvdmVyZmxvdzogaGlkZGVuO1xuICAgICAgYmFja2dyb3VuZC1jb2xvcjogd2hpdGU7XG4gICAgICBib3JkZXItcmlnaHQ6IDFweCBzb2xpZCAjZGVlMmU2ICFpbXBvcnRhbnQ7XG4gICAgICBib3JkZXItYm90dG9tOiAxcHggc29saWQgI2RlZTJlNiAhaW1wb3J0YW50O1xuICAgICAgaGVpZ2h0OiBjYWxjKDEwMHZoIC0gI3tnbG9iYWxzLiRmb290ZXItaGVpZ2h0fSk7XG4gICAgICB0cmFuc2l0aW9uOiB3aWR0aCAuMjVzIGVhc2Utb3V0O1xuICAgIH1cbiAgfVxuXG4gICY6bm90KC5ob3Zlcikge1xuICAgIC5maWx0ZXItc2lkZWJhciB7XG4gICAgICBhIHtcbiAgICAgICAgcmlnaHQ6IDEuNXJlbTtcbiAgICAgIH1cbiAgICB9XG4gICAgYXNpZGUge1xuICAgICAgbWluLXdpZHRoOiAkY29sbGFwc2VkLXdpZHRoO1xuICAgICAgbWF4LXdpZHRoOiAkY29sbGFwc2VkLXdpZHRoO1xuICAgICAgdHJhbnNpdGlvbjogbWF4LXdpZHRoIC4yNXMgZWFzZS1vdXQ7XG4gICAgICBvdmVyZmxvdzogaGlkZGVuO1xuXG4gICAgICB1bCBsaSB7XG4gICAgICAgIGEgPiBzcGFuLCBhID4gc3ZnIHtcbiAgICAgICAgICBkaXNwbGF5OiBub25lO1xuICAgICAgICB9XG4gICAgICAgIHVsIHtcbiAgICAgICAgICBkaXNwbGF5OiBub25lO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuXG4gICAgLmNvbGxhcHNlLWFsbCB7XG4gICAgICBkaXNwbGF5OiBub25lO1xuICAgIH1cblxuICAgIC5maWx0ZXIsIC5zZWFyY2gtaW5wdXQgc3ZnIHtcbiAgICAgIHRyYW5zZm9ybTogdHJhbnNsYXRlWCgtMjAuNjdyZW0pO1xuICAgICAgdHJhbnNpdGlvbjogLjI1cyBlYXNlLW91dDtcbiAgICB9XG4gIH1cblxuICAuY29sbGFwc2UtYnV0dG9uIHtcbiAgICB0cmFuc2Zvcm06IHJvdGF0ZSgtMTgwZGVnKTtcbiAgICB0cmFuc2l0aW9uOiAuNXMgZWFzZS1vdXQ7XG4gIH1cbn1cblxuOmhvc3QoLmFuaW1hdGluZykge1xuICBAaW5jbHVkZSBnbG9iYWxzLmhpZGUtc2Nyb2xsYmFycztcblxuICBhc2lkZSB7XG4gICAgQGluY2x1ZGUgZ2xvYmFscy5oaWRlLXNjcm9sbGJhcnM7XG4gIH1cbn1cblxuLmJhZGdlIHtcbiAgd2lkdGg6IDNyZW07XG59XG5cbi5uYXYtaXRlbSB7XG4gIC5zZWN0aW9uLWljb24ge1xuICAgIHdpZHRoOiAxLjVyZW07XG4gICAgaGVpZ2h0OiAxLjVyZW07XG4gICAgJi5pY29uLWFjdGl2ZSB7XG4gICAgICBmaWx0ZXI6IGludmVydCgyOCUpIHNlcGlhKDgzJSkgc2F0dXJhdGUoMjE2NCUpIGh1ZS1yb3RhdGUoMjA3ZGVnKSBicmlnaHRuZXNzKDk4JSkgY29udHJhc3QoMTAzJSk7XG4gICAgfVxuICB9XG4gIHNwYW4ge1xuICAgIGRpc3BsYXk6IGJsb2NrO1xuICAgIGZsZXgtZ3JvdzogMjtcbiAgICBwYWRkaW5nLWxlZnQ6IDAuNzVyZW07XG4gICAgcGFkZGluZy1yaWdodDogMC43NXJlbTtcbiAgfVxufVxuXG4uc2VhcmNoLWlucHV0IHtcbiAgcG9zaXRpb246IHJlbGF0aXZlO1xuXG4gIHN2ZyB7XG4gICAgcG9zaXRpb246IGFic29sdXRlO1xuICAgIHBvaW50ZXItZXZlbnRzOiBub25lO1xuICAgIGxlZnQ6IDAuNzVyZW07XG4gICAgdG9wOiAwLjc1cmVtO1xuICB9XG5cbiAgaW5wdXQge1xuICAgIHBhZGRpbmctbGVmdDogMi43NXJlbTtcbiAgICBoZWlnaHQ6IDIuNzVyZW07XG4gIH1cbn1cblxuLmxvZ28ge1xuICBoZWlnaHQ6IGdsb2JhbHMuJGhlYWRlci1oZWlnaHQ7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIHBhZGRpbmctbGVmdDogMXJlbTtcblxufVxuXG4iLCIkZm9udC1mYW1pbHktYmFzZTogSW50ZXIsIHNhbnMtc2VyaWY7XG4kaGVhZGVyLWhlaWdodDogNC41cmVtO1xuJGZvb3Rlci1oZWlnaHQ6IDUuNXJlbTtcblxuJHByaW1hcnktMjAwOiAjOTZDMEUwO1xuJHByaW1hcnktNTAwOiAjMUI3NUJCO1xuJHByaW1hcnktNjAwOiAjMTk2QUFBO1xuJHByaW1hcnktNzAwOiAjMTM1Mzg1O1xuXG4kZ3JheS01MDogI0Y5RkFGQjtcbiRncmF5LTEwMDogI0YyRjRGNztcbiRncmF5LTIwMDogI0VBRUNGMDtcbiRncmF5LTMwMDogI0QwRDVERDtcbiRncmF5LTYwMDogIzQ3NTQ2NztcbiRncmF5LTcwMDogIzM0NDA1NDtcbiRncmF5LTgwMDogIzFEMjkzOTtcbiRncmF5LTkwMDogIzEwMTgyODtcblxuXG4kbGluay1jb2xvcjogJHByaW1hcnktNTAwICFkZWZhdWx0O1xuXG5AbWl4aW4gaGlkZS1zY3JvbGxiYXJzIHtcbiAgc2Nyb2xsYmFyLXdpZHRoOiBub25lO1xuICAtbXMtb3ZlcmZsb3ctc3R5bGU6IG5vbmU7XG4gICY6Oi13ZWJraXQtc2Nyb2xsYmFyIHtcbiAgICBkaXNwbGF5OiBub25lO1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9 */"]
    });
  }
  return SidebarComponent;
})();

/***/ }),

/***/ 5770:
/*!*****************************************************!*\
  !*** ./src/app/components/steps/steps.component.ts ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   StepsComponent: () => (/* binding */ StepsComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/forms */ 8849);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ 4980);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ 1891);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ 3738);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs/operators */ 25);
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../models/template */ 9671);
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../models/template */ 5339);
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../models/template */ 7044);
/* harmony import */ var _grid_grid_component__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ../grid/grid.component */ 3150);
/* harmony import */ var _models_grid__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../models/grid */ 1708);
/* harmony import */ var _services_command_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../services/command.service */ 9167);
/* harmony import */ var _services_log_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../services/log.service */ 2553);
/* harmony import */ var _services_info_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../services/info.service */ 957);
/* harmony import */ var _services_environment_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../../services/environment.service */ 1574);
/* harmony import */ var _services_data_source_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ../../services/data-source.service */ 6678);
/* harmony import */ var _services_template_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ../../services/template.service */ 529);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var ngx_markdown__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ngx-markdown */ 1995);
/* harmony import */ var _dynamic_form_dynamic_form_component__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ../dynamic-form/dynamic-form.component */ 3439);
/* harmony import */ var _confirm_modal_confirm_modal_component__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ../confirm-modal/confirm-modal.component */ 6530);
/* harmony import */ var _modal_modal_component__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ../modal/modal.component */ 354);
/* harmony import */ var _info_info_component__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ../info/info.component */ 3636);
/* harmony import */ var _type_ahead_type_ahead_component__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ../type-ahead/type-ahead.component */ 3858);
/* harmony import */ var _directives_resize_observer_directive__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! ../../directives/resize-observer.directive */ 5067);
/* harmony import */ var _directives_log_stream_directive__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! ../../directives/log-stream.directive */ 30);
/* harmony import */ var _pipes_remove_null_pipe__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! ../../pipes/remove-null.pipe */ 8475);


























const _c0 = ["resizableHost"];
function StepsComponent_ng_container_0_ng_container_1_ng_container_18_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r5 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"]("(", ctx_r5.filteredData.length, ") ");
  }
}
function StepsComponent_ng_container_0_ng_container_1_i_20_Template(rf, ctx) {
  if (rf & 1) {
    const _r13 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "i", 33);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function StepsComponent_ng_container_0_ng_container_1_i_20_Template_i_click_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r13);
      const ctx_r12 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r12.showInfo());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
function StepsComponent_ng_container_0_ng_container_1_ng_container_21_button_1_Template(rf, ctx) {
  if (rf & 1) {
    const _r16 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "button", 39);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function StepsComponent_ng_container_0_ng_container_1_ng_container_21_button_1_Template_button_click_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r16);
      const ctx_r15 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r15.create());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "svg", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](2, "path", 40);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](3, " Add ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
function StepsComponent_ng_container_0_ng_container_1_ng_container_21_Template(rf, ctx) {
  if (rf & 1) {
    const _r18 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, StepsComponent_ng_container_0_ng_container_1_ng_container_21_button_1_Template, 4, 0, "button", 34);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "button", 35);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function StepsComponent_ng_container_0_ng_container_1_ng_container_21_Template_button_click_2_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r18);
      const ctx_r17 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r17.reload());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](3, "svg", 36);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](4, "path", 37)(5, "path", 38);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](6, " Reload");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r7.canCreate);
  }
}
function StepsComponent_ng_container_0_ng_container_1_div_22_Template(rf, ctx) {
  if (rf & 1) {
    const _r20 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 41)(1, "div", 42)(2, "theia-type-ahead", 43);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("valueChange", function StepsComponent_ng_container_0_ng_container_1_div_22_Template_theia_type_ahead_valueChange_2_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r20);
      const ctx_r19 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r19.onFilter($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
  }
  if (rf & 2) {
    const ctx_r8 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("minLength", ctx_r8.firstStep.pagination ? 3 : 1)("value", ctx_r8.filter);
  }
}
function StepsComponent_ng_container_0_ng_container_1_div_23_ng_container_1_button_1_span_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "span", 49);
  }
}
function StepsComponent_ng_container_0_ng_container_1_div_23_ng_container_1_button_1_Template(rf, ctx) {
  if (rf & 1) {
    const _r28 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "button", 47);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function StepsComponent_ng_container_0_ng_container_1_div_23_ng_container_1_button_1_Template_button_click_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r28);
      const command_r22 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
      const ctx_r26 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r26.handleSubmit(command_r22));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, StepsComponent_ng_container_0_ng_container_1_div_23_ng_container_1_button_1_span_1_Template, 1, 0, "span", 48);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const command_r22 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    const ctx_r23 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx_r23.submitting);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r23.submitting);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", command_r22.label, " ");
  }
}
function StepsComponent_ng_container_0_ng_container_1_div_23_ng_container_1_theia_confirm_modal_5_Template(rf, ctx) {
  if (rf & 1) {
    const _r32 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "theia-confirm-modal", 50);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("dismiss", function StepsComponent_ng_container_0_ng_container_1_div_23_ng_container_1_theia_confirm_modal_5_Template_theia_confirm_modal_dismiss_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r32);
      const command_r22 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
      const ctx_r30 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r30.handleConfirm($event, command_r22));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const command_r22 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    const ctx_r24 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("title", ctx_r24.firstStep.title)("visible", command_r22.show_confirmation === true);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", command_r22.confirmation_message, " ");
  }
}
function StepsComponent_ng_container_0_ng_container_1_div_23_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, StepsComponent_ng_container_0_ng_container_1_div_23_ng_container_1_button_1_Template, 3, 3, "button", 45);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](2, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](3, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](4, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](5, StepsComponent_ng_container_0_ng_container_1_div_23_ng_container_1_theia_confirm_modal_5_Template, 2, 3, "theia-confirm-modal", 46);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const command_r22 = ctx.$implicit;
    const ctx_r21 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](2, 2, ctx_r21.isNew$) && command_r22.new_hide) && !(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](3, 4, ctx_r21.isNew$) === false && !ctx_r21.isReadOnly && command_r22.editable_hide) && !(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](4, 6, ctx_r21.isNew$) === false && ctx_r21.isReadOnly && command_r22.readonly_hide));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", command_r22.require_confirmation);
  }
}
function StepsComponent_ng_container_0_ng_container_1_div_23_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 44);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, StepsComponent_ng_container_0_ng_container_1_div_23_ng_container_1_Template, 6, 8, "ng-container", 6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r9 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r9.firstStep.commands);
  }
}
function StepsComponent_ng_container_0_ng_container_1_markdown_26_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "markdown", 51);
  }
  if (rf & 2) {
    const ctx_r10 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("data", ctx_r10.firstStep.description);
  }
}
function StepsComponent_ng_container_0_ng_container_1_p_27_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "p", 52);
  }
  if (rf & 2) {
    const ctx_r11 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("innerHTML", ctx_r11.firstStep.description, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsanitizeHtml"]);
  }
}
function StepsComponent_ng_container_0_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    const _r35 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 17);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("resize", function StepsComponent_ng_container_0_ng_container_1_Template_div_resize_1_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r35);
      const ctx_r34 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r34.onHeaderResize($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "div", 18)(3, "div", 19);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "svg", 20);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](5, "path", 21);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](6, "svg", 22);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](7, "path", 23);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceHTML"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](8, "div");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](9);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](10, "svg", 22);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](11, "path", 23);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceHTML"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](12, "div");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](13);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](14, "div", 24)(15, "div", 25)(16, "h3");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](17);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](18, StepsComponent_ng_container_0_ng_container_1_ng_container_18_Template, 2, 1, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](19, "div", 26);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](20, StepsComponent_ng_container_0_ng_container_1_i_20_Template, 1, 0, "i", 27);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](21, StepsComponent_ng_container_0_ng_container_1_ng_container_21_Template, 7, 1, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](22, StepsComponent_ng_container_0_ng_container_1_div_22_Template, 3, 2, "div", 28);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](23, StepsComponent_ng_container_0_ng_container_1_div_23_Template, 2, 1, "div", 29);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](24, "div", 24)(25, "div", 30);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](26, StepsComponent_ng_container_0_ng_container_1_markdown_26_Template, 1, 1, "markdown", 31);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](27, StepsComponent_ng_container_0_ng_container_1_p_27_Template, 1, 1, "p", 32);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](9);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](ctx_r1.sectionLabel);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](ctx_r1.actionLabel);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"]("", ctx_r1.firstStep.title, " ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r1.data && ctx_r1.firstStep.type === ctx_r1.TheiaStep.Grid);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r1.firstStep.info);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r1.firstStep.type === ctx_r1.TheiaStep.Grid);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r1.firstStep.type === ctx_r1.TheiaStep.Grid);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r1.firstStep.type === ctx_r1.TheiaStep.Form && !(ctx_r1.firstStep.controls == null ? null : ctx_r1.firstStep.controls.length));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r1.firstStep.allowMarkdown);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !ctx_r1.firstStep.allowMarkdown);
  }
}
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_theia_dynamic_form_3_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "theia-dynamic-form", 62);
  }
  if (rf & 2) {
    const step_r36 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3).$implicit;
    const ctx_r43 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵstyleProp"]("max-height", ctx_r43.headerHeight ? "calc(100vh - 4.5rem - 5.5rem - 3rem - 7.93rem - " + ctx_r43.headerHeight + "px)" : "");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formGroup", ctx_r43.formGroup)("step", step_r36)("selectedId", ctx_r43.selectedRowId);
  }
}
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_theia_grid_4_Template(rf, ctx) {
  if (rf & 1) {
    const _r50 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "theia-grid", 63);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("selected", function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_theia_grid_4_Template_theia_grid_selected_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r50);
      const ctx_r49 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](5);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r49.selected($event));
    })("sort", function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_theia_grid_4_Template_theia_grid_sort_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r50);
      const ctx_r51 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](5);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r51.sortBy($event));
    })("pageChange", function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_theia_grid_4_Template_theia_grid_pageChange_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r50);
      const ctx_r52 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](5);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r52.onPageChange($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const step_r36 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3).$implicit;
    const ctx_r44 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵstyleProp"]("max-height", ctx_r44.headerHeight ? "calc(100vh - 4.5rem - 5.5rem - 5rem - " + ctx_r44.headerHeight + "px)" : "");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formGroup", ctx_r44.formGroup)("step", step_r36)("data", ctx_r44.filteredData)("loading", ctx_r44.loading)("paginationData", ctx_r44.paginationData)("selectedRowId", ctx_r44.selectedRowId)("sortKey", ctx_r44.sortKey)("sortOrder", ctx_r44.sortOrder);
  }
}
const _c1 = function () {
  return {
    clipboard: true
  };
};
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_5_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "div", 64);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](2, "markdown");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](3, "language");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](4, "json");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](5, "removeNull");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r45 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵstyleProp"]("max-height", ctx_r45.headerHeight ? "calc(100vh - 4.5rem - 5.5rem - 11.3rem - " + ctx_r45.headerHeight + "px)" : "");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("innerHTML", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind2"](2, 3, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind2"](3, 6, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](4, 9, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](5, 11, ctx_r45.formGroup.value)), "json"), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction0"](13, _c1)), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsanitizeHtml"]);
  }
}
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_6_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div")(1, "div", 65)(2, "div", 66);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](3, "div", 67);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "div", 68)(5, "div", 69)(6, "span", 70);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](7, "Loading...");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()()()()();
  }
  if (rf & 2) {
    const step_r36 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3).$implicit;
    const ctx_r46 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵstyleProp"]("max-height", ctx_r46.headerHeight ? "calc(100vh - 4.5rem - 5.5rem - 5rem - " + ctx_r46.headerHeight + "px)" : "");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("dataSource", step_r36.datasource);
  }
}
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_button_2_Template(rf, ctx) {
  if (rf & 1) {
    const _r59 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "button", 75);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_button_2_Template_button_click_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r59);
      const ctx_r58 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](6);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r58.back());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Close ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_button_3_Template(rf, ctx) {
  if (rf & 1) {
    const _r61 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "button", 13);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_button_3_Template_button_click_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r61);
      const ctx_r60 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](6);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r60.next());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Next ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
}
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_ng_container_4_ng_container_1_button_1_span_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "span", 49);
  }
}
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_ng_container_4_ng_container_1_button_1_Template(rf, ctx) {
  if (rf & 1) {
    const _r69 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "button", 47);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_ng_container_4_ng_container_1_button_1_Template_button_click_0_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r69);
      const command_r63 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
      const ctx_r67 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](7);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r67.handleSubmit(command_r63));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_ng_container_4_ng_container_1_button_1_span_1_Template, 1, 0, "span", 48);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const command_r63 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    const ctx_r64 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("disabled", ctx_r64.submitting);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r64.submitting);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", command_r63.label, " ");
  }
}
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_ng_container_4_ng_container_1_theia_confirm_modal_5_Template(rf, ctx) {
  if (rf & 1) {
    const _r73 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "theia-confirm-modal", 50);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("dismiss", function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_ng_container_4_ng_container_1_theia_confirm_modal_5_Template_theia_confirm_modal_dismiss_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r73);
      const command_r63 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
      const ctx_r71 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](7);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r71.handleConfirm($event, command_r63));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const command_r63 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]().$implicit;
    const step_r36 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](5).$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("title", step_r36.title)("visible", command_r63.show_confirmation === true);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"](" ", command_r63.confirmation_message, " ");
  }
}
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_ng_container_4_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_ng_container_4_ng_container_1_button_1_Template, 3, 3, "button", 45);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](2, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](3, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](4, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](5, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_ng_container_4_ng_container_1_theia_confirm_modal_5_Template, 2, 3, "theia-confirm-modal", 46);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const command_r63 = ctx.$implicit;
    const ctx_r62 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](2, 2, ctx_r62.isNew$) && command_r63.new_hide) && !(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](3, 4, ctx_r62.isNew$) === false && !ctx_r62.isReadOnly && command_r63.editable_hide) && !(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](4, 6, ctx_r62.isNew$) === false && ctx_r62.isReadOnly && command_r63.readonly_hide));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", command_r63.require_confirmation);
  }
}
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_ng_container_4_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_ng_container_4_ng_container_1_Template, 6, 8, "ng-container", 6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const step_r36 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4).$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", step_r36.commands);
  }
}
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 71)(1, "div", 72);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_button_2_Template, 2, 0, "button", 73);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_button_3_Template, 2, 0, "button", 74);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_ng_container_4_Template, 2, 1, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r77 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](3);
    const first_r39 = ctx_r77.first;
    const last_r38 = ctx_r77.last;
    const step_r36 = ctx_r77.$implicit;
    const ctx_r47 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !first_r39);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", !last_r38);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", last_r38 && step_r36.type === ctx_r47.TheiaStep.Form);
  }
}
const _c2 = function (a0) {
  return {
    "grid": a0
  };
};
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 56)(1, "div", 57)(2, "form", 58);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_theia_dynamic_form_3_Template, 1, 5, "theia-dynamic-form", 59);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](4, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_theia_grid_4_Template, 1, 10, "theia-grid", 60);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](5, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_5_Template, 6, 14, "div", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](6, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_6_Template, 8, 3, "div", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](7, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_div_7_Template, 5, 3, "div", 61);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
  }
  if (rf & 2) {
    const step_r36 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2).$implicit;
    const ctx_r41 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction1"](7, _c2, step_r36.type === ctx_r41.TheiaStep.Grid));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("formGroup", ctx_r41.formGroup);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", step_r36.type === ctx_r41.TheiaStep.Form);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", step_r36.type === ctx_r41.TheiaStep.Grid);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", step_r36.type === ctx_r41.TheiaStep.Json);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", step_r36.type === ctx_r41.TheiaStep.Log);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", step_r36.type !== ctx_r41.TheiaStep.Grid && step_r36.type !== ctx_r41.TheiaStep.Log);
  }
}
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_3_Template(rf, ctx) {
  if (rf & 1) {
    const _r80 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 76);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("mousedown", function StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_3_Template_div_mousedown_0_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r80);
      const ctx_r79 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r79.resizerMouseDown($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "i", 77);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const ctx_r42 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵstyleProp"]("left", ctx_r42.resizerPosition + "%");
  }
}
function StepsComponent_ng_container_0_ng_container_15_ng_container_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](1, "div", 53);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_2_Template, 8, 9, "div", 54);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](3, StepsComponent_ng_container_0_ng_container_15_ng_container_1_div_3_Template, 2, 2, "div", 55);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r81 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    const i_r37 = ctx_r81.index;
    const step_r36 = ctx_r81.$implicit;
    const first_r39 = ctx_r81.first;
    const ctx_r40 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵstyleProp"]("width", ctx_r40.columnWidths[i_r37] + "%");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("className", "col-" + 12 / (ctx_r40.currentStepIndex + 1));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", step_r36 && (step_r36.type !== ctx_r40.TheiaStep.Form || (step_r36.controls == null ? null : step_r36.controls.length)));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", first_r39 && ctx_r40.currentStepIndex > 0);
  }
}
function StepsComponent_ng_container_0_ng_container_15_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, StepsComponent_ng_container_0_ng_container_15_ng_container_1_Template, 4, 5, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const step_r36 = ctx.$implicit;
    const i_r37 = ctx.index;
    const ctx_r3 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", i_r37 <= ctx_r3.currentStepIndex && step_r36);
  }
}
function StepsComponent_ng_container_0_theia_info_16_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](0, "theia-info");
  }
}
const _c3 = function (a0, a1, a2) {
  return {
    "info-open": a0,
    "info-closed": a1,
    "info-disabled": a2
  };
};
function StepsComponent_ng_container_0_Template(rf, ctx) {
  if (rf & 1) {
    const _r83 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](1, StepsComponent_ng_container_0_ng_container_1_Template, 28, 10, "ng-container", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "div", 1)(3, "div", 2)(4, "div", 3);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](5, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](6, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](7, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](8, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](9, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](10, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](11, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](12, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](13, "div", 4, 5);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("mousemove", function StepsComponent_ng_container_0_Template_div_mousemove_13_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r83);
      const ctx_r82 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r82.resizerMouseMove($event));
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](15, StepsComponent_ng_container_0_ng_container_15_Template, 2, 1, "ng-container", 6);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](16, StepsComponent_ng_container_0_theia_info_16_Template, 1, 0, "theia-info", 0);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](17, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](18, "theia-modal", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](19, 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](20, "h5", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](21, "Log");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](22, "button", 10);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function StepsComponent_ng_container_0_Template_button_click_22_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r83);
      const ctx_r84 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r84.modalClose());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](23, 11);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](24, "pre");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](25);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](26, 12);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](27, "button", 13);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function StepsComponent_ng_container_0_Template_button_click_27_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵrestoreView"](_r83);
      const ctx_r85 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresetView"](ctx_r85.modalClose());
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](28, "Ok");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](29, "theia-modal", 14);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](30, 8);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](31, "h5", 9);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](32, "Please wait");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerStart"](33, 11);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](34, "div", 15);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](35, "div", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementContainerEnd"]();
  }
  if (rf & 2) {
    const ctx_r0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx_r0.firstStep);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵstyleProp"]("height", ctx_r0.headerHeight ? "calc(100% - " + ctx_r0.headerHeight + "px)" : "");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngClass", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction3"](27, _c3, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](5, 9, ctx_r0.infoText$) && _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](6, 11, ctx_r0.infoEnabled$) === true, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](7, 13, ctx_r0.infoText$) && _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](8, 15, ctx_r0.infoEnabled$) === false, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](9, 17, ctx_r0.infoEnabled$) === false || _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](10, 19, ctx_r0.infoText$) === "" || _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](11, 21, ctx_r0.infoText$) === null || _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](12, 23, ctx_r0.infoText$) === undefined));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](11);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", ctx_r0.steps);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](17, 25, ctx_r0.infoText$));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("visible", ctx_r0.showLog);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](7);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate1"]("      ", ctx_r0.log, "\n    ");
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("visible", ctx_r0.submitting);
  }
}
let StepsComponent = /*#__PURE__*/(() => {
  class StepsComponent {
    get cursor() {
      if (this.mouseDown) {
        return 'col-resize';
      }
      return '';
    }
    onMouseUp() {
      this.mouseDown = false;
    }
    constructor(fb, commandService, logService, infoService, environmentService, dataSourceService, cdr, templateService) {
      this.fb = fb;
      this.commandService = commandService;
      this.logService = logService;
      this.infoService = infoService;
      this.environmentService = environmentService;
      this.dataSourceService = dataSourceService;
      this.cdr = cdr;
      this.templateService = templateService;
      this.steps = [];
      this.actionId = '';
      this.sectionLabel = '';
      this.actionLabel = '';
      this.stepChanged = new _angular_core__WEBPACK_IMPORTED_MODULE_0__.EventEmitter();
      this.submitting = false;
      this.currentStepIndex = 0;
      this.TheiaStep = _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaStep;
      this.showLog = false;
      this.log = '';
      this.loading = false;
      this.data = [];
      this.filteredData = [];
      this.filter = '';
      this.sortKey = '';
      this.sortOrder = _models_grid__WEBPACK_IMPORTED_MODULE_2__.SortOrder.Asc;
      this.currentPage = 1;
      this.selectedRowId = '';
      this.mouseDown = false;
      this.columnWidths = [];
      this.formGroup = fb.group({});
      this.isNew$ = commandService.isNew$;
      this.infoText$ = infoService.data$;
      this.infoEnabled$ = infoService.enabled$;
    }
    get isReadOnly() {
      return !!this.currentStep.readonly;
    }
    get currentStep() {
      return this.steps[this.currentStepIndex];
    }
    get firstStep() {
      return this.steps[0];
    }
    get canCreate() {
      return !(this.firstStep?.single_value && this.data.length > 0) && !this.firstStep?.hide_add && !this.firstStep?.readonly;
    }
    ngOnInit() {
      this.formGroup.reset();
      this.sortKey = '';
      this.sortOrder = _models_grid__WEBPACK_IMPORTED_MODULE_2__.SortOrder.Asc;
      this.loadData();
    }
    ngOnChanges(changes) {
      this.formGroup = this.fb.group({});
      this.currentStepIndex = 0;
      this.showLog = false;
      this.log = '';
      this.commandService.isNew = false;
      this.resizerPosition = undefined;
      this.columnWidths = [];
      this.loadData();
    }
    handleConfirm(confirmed, command) {
      command.show_confirmation = false;
      if (confirmed) {
        this.sendPayload(command);
      }
    }
    handleSubmit(command) {
      this.markFormGroupTouched(this.formGroup);
      if (this.formGroup.invalid) {
        return;
      }
      if (command.require_confirmation) {
        command.show_confirmation = true;
        return;
      }
      this.sendPayload(command);
    }
    sendPayload(command) {
      this.submitting = true;
      const payload = {
        ...command.command,
        ...this.removeExtraValues(this.formatValues(this.formGroup.value))
      };
      this.commandService.runCommand(payload).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_3__.switchMap)(resp => this.logService.getLog(resp.log_file))).subscribe(log => {
        this.log = log;
        this.submitting = false;
        this.showLog = true;
        this.commandService.isNew = false;
        if (this.actionId === 'Environments') {
          this.environmentService.getEnvironments().subscribe();
        }
        if (this.grid) {
          this.loadData();
        }
      }, () => {
        this.submitting = false;
      });
    }
    next() {
      if (this.currentStepIndex === 0) {
        this.currentStepIndex++;
      }
      if (this.currentStep.readonly && !this.commandService.isNew) {
        this.formGroup.disable();
      } else {
        this.formGroup.enable();
      }
      this.markFormGroupTouched(this.formGroup);
      if (this.formGroup.invalid) {
        return;
      }
      this.stepChanged.emit(this.currentStepIndex);
    }
    back() {
      this.currentStepIndex--;
      if (this.currentStep.readonly && !this.commandService.isNew) {
        this.formGroup.disable();
      } else {
        this.formGroup.enable();
      }
      this.stepChanged.emit(this.currentStepIndex);
    }
    modalClose() {
      this.showLog = false;
    }
    selected(event) {
      if (this.selectedRowId === '' && event.data?.id === this.selectedRowId) {
        return;
      }
      this.commandService.isNew = event.isNew;
      if (this.firstStep?.dynamic_template) {
        const url = this.parseDynamicUrl(event.isNew ? this.firstStep.default_template : this.firstStep.dynamic_template, event.data);
        this.templateService.loadDynamicTemplate(url).subscribe(step => {
          this.steps[1] = step;
          this.rowSelected(event.data);
          this.next();
        });
        return;
      } else {
        this.rowSelected(event.data);
        this.next();
      }
    }
    reload() {
      this.currentStepIndex = 0;
      this.stepChanged.emit(this.currentStepIndex);
      this.rowSelected({});
      const params = this.firstStep?.pagination ? {
        start: (this.currentPage - 1) * (this.paginationData?.limit ?? 1) + 1,
        search: this.filter
      } : undefined;
      this.loadData(params);
    }
    loadData(params = {}) {
      if (!this.firstStep) {
        return;
      }
      this.loading = true;
      const paginationData$ = this.firstStep?.pagination ? this.dataSourceService.getData(this.firstStep.pagination, true, params) : (0,rxjs__WEBPACK_IMPORTED_MODULE_4__.of)({
        size: 0,
        limit: 0
      });
      paginationData$.pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_5__.tap)(data => {
        this.paginationData = data;
      }), (0,rxjs_operators__WEBPACK_IMPORTED_MODULE_6__.switchMapTo)(this.dataSourceService.getData(this.firstStep.datasource, this.firstStep.env_param_required, params))).subscribe(response => {
        response.forEach((item, index) => item.id = index.toString());
        this.loading = false;
        this.data = response;
        if (this.firstStep?.pagination) {
          this.filteredData = this.data;
        } else {
          this.onFilter('');
        }
      });
    }
    onFilter(filter) {
      this.filter = filter;
      if (this.firstStep?.pagination) {
        this.loadData({
          start: (this.currentPage - 1) * (this.paginationData?.limit ?? 1) + 1,
          search: this.filter
        });
        this.filteredData = this.data;
        this.sort();
      } else {
        this.filteredData = this.data.filter(item => {
          return Object.values(item).some(value => {
            return value?.toString().toLowerCase().includes(filter?.toString().toLowerCase());
          });
        });
        this.sort();
      }
    }
    sort() {
      if (!this.sortKey) {
        return;
      }
      this.filteredData.sort((a, b) => (a[this.sortKey] || '').toString().localeCompare((b[this.sortKey] || '').toString()));
      if (this.sortOrder === _models_grid__WEBPACK_IMPORTED_MODULE_2__.SortOrder.Desc) {
        this.filteredData.reverse();
      }
    }
    showInfo() {
      this.infoService.showInfoPanel(this.firstStep?.info || '');
    }
    create() {
      this.selected({
        isNew: true,
        data: {}
      });
    }
    rowSelected(row = {}) {
      if (this.firstStep?.readonly) {
        return;
      }
      this.selectedRowId = row.id;
      this.addControls(row);
      this.formGroup.reset();
      this.resetFormArrays();
      Object.entries(row).forEach(([key, value]) => {
        const control = this.formGroup.get(key);
        if (control) {
          try {
            if (Array.isArray(value) && value.every(item => this.isObject(item))) {
              value.forEach(v => {
                const values = Object.entries(v).reduce((prev, [currKey, currValue]) => {
                  let newValue = currValue;
                  if (this.isObject(currValue) && currValue.type === _models_template__WEBPACK_IMPORTED_MODULE_7__.TheiaType.DataOption) {
                    newValue = currValue.value;
                  }
                  prev[currKey] = newValue;
                  return prev;
                }, {});
                control.push(this.fb.group(values));
              });
            } else {
              control.setValue(value, {
                onlySelf: true
              });
            }
          } catch (e) {
            if (e instanceof TypeError && control instanceof _angular_forms__WEBPACK_IMPORTED_MODULE_8__.UntypedFormArray) {
              control.setValue([]);
            }
          }
        }
      });
      this.cdr.detectChanges();
    }
    addControls(row) {
      Object.keys(row).forEach(key => {
        if (!this.formGroup.get(key)) {
          if (Array.isArray(row[key]) && row[key].every(item => this.isObject(item))) {
            this.formGroup.addControl(key, this.fb.array([]));
          } else {
            this.formGroup.addControl(key, this.fb.control(null));
          }
        }
      });
    }
    resetFormArrays() {
      Object.values(this.formGroup.controls).forEach(control => {
        if (control instanceof _angular_forms__WEBPACK_IMPORTED_MODULE_8__.UntypedFormArray) {
          control.clear();
        }
      });
    }
    parseDynamicUrl(url, context = {}) {
      const rx = /\${(.*?)}/g;
      return url.replace(rx, (_, key) => context[key]);
    }
    isObject(value) {
      return typeof value === 'object' && !Array.isArray(value) && value !== null;
    }
    sortBy(column) {
      if (this.sortKey === column) {
        this.sortOrder = this.sortOrder === _models_grid__WEBPACK_IMPORTED_MODULE_2__.SortOrder.Asc ? _models_grid__WEBPACK_IMPORTED_MODULE_2__.SortOrder.Desc : _models_grid__WEBPACK_IMPORTED_MODULE_2__.SortOrder.Asc;
      } else {
        this.sortOrder = _models_grid__WEBPACK_IMPORTED_MODULE_2__.SortOrder.Asc;
        this.sortKey = column;
      }
      this.sort();
    }
    onPageChange(page) {
      this.currentPage = page;
      this.loadData({
        start: (this.currentPage - 1) * (this.paginationData?.limit ?? 1) + 1,
        search: this.filter
      });
    }
    markFormGroupTouched(formGroup) {
      formGroup.markAsTouched();
      Object.values(formGroup.controls).forEach(control => {
        control.markAsTouched();
        if (control.controls) {
          this.markFormGroupTouched(control);
        }
      });
    }
    formatValues(payload) {
      const controlReducer = (prev, curr) => {
        switch (curr.type) {
          case _models_template__WEBPACK_IMPORTED_MODULE_9__.TheiaControl.Toggle:
            prev[curr.id] = Boolean(prev[curr.id]).toString();
            break;
          case _models_template__WEBPACK_IMPORTED_MODULE_9__.TheiaControl.KeyValue:
            const value = prev[curr.id].reduce((prev, curr) => {
              prev[curr.key] = curr.value;
              return prev;
            }, {});
            prev[curr.id] = JSON.stringify(value).toString().replace(/"/g, '\\"');
            break;
          case _models_template__WEBPACK_IMPORTED_MODULE_9__.TheiaControl.CompositeModule:
            curr.modules?.forEach(module => {
              prev[module.id] = Boolean(prev[module.id]).toString();
              module.controls.reduce(controlReducer, prev);
            });
            break;
        }
        return prev;
      };
      return this.currentStep.controls?.reduce(controlReducer, payload) || {};
    }
    removeExtraValues(payload) {
      const ids = [];
      const idArgMap = this.currentStep?.controls?.reduce((prev, curr) => {
        const addControl = control => {
          ids.push(control.id);
          prev[control.id] = control.cli_arg || control.id;
        };
        if (curr.type === _models_template__WEBPACK_IMPORTED_MODULE_9__.TheiaControl.CompositeModule) {
          curr.modules?.forEach(module => {
            addControl(module);
            module.controls.forEach(addControl);
          });
        } else {
          addControl(curr);
        }
        return prev;
      }, {}) || {};
      const result = {};
      Object.entries(payload).forEach(([key, value]) => {
        const validKey = ids.includes(key);
        if (validKey && value) {
          const arg = idArgMap[key];
          const control = this.findControlByKey(key);
          if (control && control.type === _models_template__WEBPACK_IMPORTED_MODULE_9__.TheiaControl.CompositeGroup) {
            result[arg] = value;
            return;
          } else if (Array.isArray(value)) {
            value = value.map(val => {
              if (val.type === _models_template__WEBPACK_IMPORTED_MODULE_7__.TheiaType.DataOption) {
                return val.value;
              }
              return val;
            });
          } else if (value.type === _models_template__WEBPACK_IMPORTED_MODULE_7__.TheiaType.DataOption) {
            value = value.value;
          }
          result[arg] = Array.isArray(value) ? value.toString() : value;
        }
      });
      return result;
    }
    findControlByKey(id) {
      return this.currentStep.controls?.find(control => control.id === id);
    }
    resizerMouseDown(event) {
      if (event.button !== 0) {
        return;
      }
      this.mouseDown = true;
    }
    resizerMouseMove(event) {
      if (this.mouseDown) {
        event.preventDefault();
        event.stopPropagation();
        const left = this.resizableHost.nativeElement.getBoundingClientRect().left;
        const percent = (event.clientX - left) * 100 / this.resizableHost.nativeElement.getBoundingClientRect().width;
        this.resizerPosition = Math.min(Math.max(percent, 10), 90);
        this.columnWidths = [this.resizerPosition, 100 - this.resizerPosition];
      }
    }
    onHeaderResize(event) {
      this.headerHeight = event.height;
    }
    static #_ = this.ɵfac = function StepsComponent_Factory(t) {
      return new (t || StepsComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_forms__WEBPACK_IMPORTED_MODULE_8__.UntypedFormBuilder), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_command_service__WEBPACK_IMPORTED_MODULE_10__.CommandService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_log_service__WEBPACK_IMPORTED_MODULE_11__.LogService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_info_service__WEBPACK_IMPORTED_MODULE_12__.InfoService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_environment_service__WEBPACK_IMPORTED_MODULE_13__.EnvironmentService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_data_source_service__WEBPACK_IMPORTED_MODULE_14__.DataSourceService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.ChangeDetectorRef), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_template_service__WEBPACK_IMPORTED_MODULE_15__.TemplateService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: StepsComponent,
      selectors: [["theia-steps"]],
      viewQuery: function StepsComponent_Query(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵviewQuery"](_grid_grid_component__WEBPACK_IMPORTED_MODULE_16__.GridComponent, 5);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵviewQuery"](_c0, 5);
        }
        if (rf & 2) {
          let _t;
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.grid = _t.first);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.resizableHost = _t.first);
        }
      },
      hostVars: 2,
      hostBindings: function StepsComponent_HostBindings(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("mouseup", function StepsComponent_mouseup_HostBindingHandler() {
            return ctx.onMouseUp();
          }, false, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresolveDocument"]);
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵstyleProp"]("cursor", ctx.cursor);
        }
      },
      inputs: {
        steps: "steps",
        actionId: "actionId",
        sectionLabel: "sectionLabel",
        actionLabel: "actionLabel"
      },
      outputs: {
        stepChanged: "stepChanged"
      },
      features: [_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵNgOnChangesFeature"]],
      decls: 1,
      vars: 1,
      consts: [[4, "ngIf"], [1, "row", "flex-nowrap"], [1, "col-12", "d-flex", "flex-nowrap"], [3, "ngClass"], [1, "row", "position-relative", 3, "mousemove"], ["resizableHost", ""], [4, "ngFor", "ngForOf"], ["classes", "modal-xl modal-dialog-scrollable modal-dialog-centered", 3, "visible"], ["slot", "header"], [1, "modal-title"], ["type", "button", "data-bs-dismiss", "modal", "aria-label", "Close", 1, "btn-close", 3, "click"], ["slot", "body"], ["slot", "footer"], ["type", "button", 1, "btn", "btn-primary", 3, "click"], ["classes", "modal modal-dialog-scrollable modal-dialog-centered", 3, "visible"], [1, "progress"], ["role", "progressbar", "aria-valuenow", "100", "aria-valuemin", "100", "aria-valuemax", "100", 1, "progress-bar", "progress-bar-striped", "progress-bar-animated", 2, "width", "100%"], ["theiaResizeObserver", "", 1, "mb-4", "step-header", 3, "resize"], [1, "row", "mb-3"], [1, "col", "breadcrumbs"], ["xmlns", "http://www.w3.org/2000/svg", "width", "20", "height", "20", "viewBox", "0 0 20 20", "fill", "none"], ["d", "M6.66667 14.1668H13.3333M9.18141 2.30345L3.52949 6.69939C3.15168 6.99324 2.96278 7.14017 2.82669 7.32417C2.70614 7.48716 2.61633 7.67078 2.56169 7.866C2.5 8.08639 2.5 8.3257 2.5 8.80433V14.8334C2.5 15.7669 2.5 16.2336 2.68166 16.5901C2.84144 16.9037 3.09641 17.1587 3.41002 17.3185C3.76654 17.5001 4.23325 17.5001 5.16667 17.5001H14.8333C15.7668 17.5001 16.2335 17.5001 16.59 17.3185C16.9036 17.1587 17.1586 16.9037 17.3183 16.5901C17.5 16.2336 17.5 15.7669 17.5 14.8334V8.80433C17.5 8.3257 17.5 8.08639 17.4383 7.866C17.3837 7.67078 17.2939 7.48716 17.1733 7.32417C17.0372 7.14017 16.8483 6.99324 16.4705 6.69939L10.8186 2.30345C10.5258 2.07574 10.3794 1.96189 10.2178 1.91812C10.0752 1.87951 9.92484 1.87951 9.78221 1.91812C9.62057 1.96189 9.47418 2.07574 9.18141 2.30345Z", "stroke", "#667085", "stroke-width", "1.66667", "stroke-linecap", "round", "stroke-linejoin", "round"], ["xmlns", "http://www.w3.org/2000/svg", "width", "16", "height", "16", "viewBox", "0 0 16 16", "fill", "none"], ["d", "M6 12L10 8L6 4", "stroke", "#D0D5DD", "stroke-width", "1.33333", "stroke-linecap", "round", "stroke-linejoin", "round"], [1, "row"], [1, "col", "d-flex", "align-items-center"], [1, "col-2", "d-flex", "justify-content-end", "align-items-center"], ["class", "mx-2 info-btn bi bi-info-circle fs-4", 3, "click", 4, "ngIf"], ["class", "col-3", 4, "ngIf"], ["class", "col text-end", 4, "ngIf"], [1, "col"], [3, "data", 4, "ngIf"], [3, "innerHTML", 4, "ngIf"], [1, "mx-2", "info-btn", "bi", "bi-info-circle", "fs-4", 3, "click"], ["class", "btn btn-primary btn-sm", "type", "button", 3, "click", 4, "ngIf"], [1, "btn", "btn-primary", "btn-sm", "ms-1", 3, "click"], ["xmlns", "http://www.w3.org/2000/svg", "width", "20", "height", "20", "fill", "currentColor", "viewBox", "0 0 16 16", 1, "bi", "bi-arrow-clockwise"], ["fill-rule", "evenodd", "d", "M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"], ["d", "M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"], ["type", "button", 1, "btn", "btn-primary", "btn-sm", 3, "click"], ["d", "M10 6.66667V13.3333M6.66667 10H13.3333M6.5 17.5H13.5C14.9001 17.5 15.6002 17.5 16.135 17.2275C16.6054 16.9878 16.9878 16.6054 17.2275 16.135C17.5 15.6002 17.5 14.9001 17.5 13.5V6.5C17.5 5.09987 17.5 4.3998 17.2275 3.86502C16.9878 3.39462 16.6054 3.01217 16.135 2.77248C15.6002 2.5 14.9001 2.5 13.5 2.5H6.5C5.09987 2.5 4.3998 2.5 3.86502 2.77248C3.39462 3.01217 3.01217 3.39462 2.77248 3.86502C2.5 4.3998 2.5 5.09987 2.5 6.5V13.5C2.5 14.9001 2.5 15.6002 2.77248 16.135C3.01217 16.6054 3.39462 16.9878 3.86502 17.2275C4.3998 17.5 5.09987 17.5 6.5 17.5Z", "stroke", "white", "stroke-width", "1.66667", "stroke-linecap", "round", "stroke-linejoin", "round"], [1, "col-3"], [1, "search-input"], ["placeHolder", "Search...", 3, "minLength", "value", "valueChange"], [1, "col", "text-end"], ["class", "btn btn-primary ms-2", 3, "disabled", "click", 4, "ngIf"], [3, "title", "visible", "dismiss", 4, "ngIf"], [1, "btn", "btn-primary", "ms-2", 3, "disabled", "click"], ["class", "spinner-border spinner-border-sm", 4, "ngIf"], [1, "spinner-border", "spinner-border-sm"], [3, "title", "visible", "dismiss"], [3, "data"], [3, "innerHTML"], [3, "className"], ["class", "text-center step-body", 3, "ngClass", 4, "ngIf"], ["class", "resizer", 3, "left", "mousedown", 4, "ngIf"], [1, "text-center", "step-body", 3, "ngClass"], [1, "text-start"], ["novalidate", "", 3, "formGroup"], [3, "formGroup", "step", "selectedId", "max-height", 4, "ngIf"], [3, "max-height", "formGroup", "step", "data", "loading", "paginationData", "selectedRowId", "sortKey", "sortOrder", "selected", "sort", "pageChange", 4, "ngIf"], ["class", "step-footer", 4, "ngIf"], [3, "formGroup", "step", "selectedId"], [3, "formGroup", "step", "data", "loading", "paginationData", "selectedRowId", "sortKey", "sortOrder", "selected", "sort", "pageChange"], [1, "json", 3, "innerHTML"], [1, "overflow-auto", "d-flex", "flex-column-reverse"], [1, "p-3"], ["theiaLogStream", "", 3, "dataSource"], [1, "text-center"], ["role", "status", 1, "spinner-border", "spinner-border-sm", "text-primary", "mt-3"], [1, "visually-hidden"], [1, "step-footer"], [1, "col", "text-start"], ["class", "btn btn-outline-secondary", "type", "button", 3, "click", 4, "ngIf"], ["class", "btn btn-primary", "type", "button", 3, "click", 4, "ngIf"], ["type", "button", 1, "btn", "btn-outline-secondary", 3, "click"], [1, "resizer", 3, "mousedown"], [1, "bi", "bi-grip-vertical"]],
      template: function StepsComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](0, StepsComponent_ng_container_0_Template, 36, 31, "ng-container", 0);
        }
        if (rf & 2) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngIf", ctx.steps.length);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_17__.NgClass, _angular_common__WEBPACK_IMPORTED_MODULE_17__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_17__.NgIf, _angular_forms__WEBPACK_IMPORTED_MODULE_8__["ɵNgNoValidate"], _angular_forms__WEBPACK_IMPORTED_MODULE_8__.NgControlStatusGroup, _angular_forms__WEBPACK_IMPORTED_MODULE_8__.FormGroupDirective, ngx_markdown__WEBPACK_IMPORTED_MODULE_18__.MarkdownComponent, _dynamic_form_dynamic_form_component__WEBPACK_IMPORTED_MODULE_19__.DynamicFormComponent, _grid_grid_component__WEBPACK_IMPORTED_MODULE_16__.GridComponent, _confirm_modal_confirm_modal_component__WEBPACK_IMPORTED_MODULE_20__.ConfirmModalComponent, _modal_modal_component__WEBPACK_IMPORTED_MODULE_21__.ModalComponent, _info_info_component__WEBPACK_IMPORTED_MODULE_22__.InfoComponent, _type_ahead_type_ahead_component__WEBPACK_IMPORTED_MODULE_23__.TypeAheadComponent, _directives_resize_observer_directive__WEBPACK_IMPORTED_MODULE_24__.ResizeObserverDirective, _directives_log_stream_directive__WEBPACK_IMPORTED_MODULE_25__.LogStreamDirective, _angular_common__WEBPACK_IMPORTED_MODULE_17__.AsyncPipe, _angular_common__WEBPACK_IMPORTED_MODULE_17__.JsonPipe, ngx_markdown__WEBPACK_IMPORTED_MODULE_18__.LanguagePipe, ngx_markdown__WEBPACK_IMPORTED_MODULE_18__.MarkdownPipe, _pipes_remove_null_pipe__WEBPACK_IMPORTED_MODULE_26__.RemoveNullPipe],
      styles: ["pre[_ngcontent-%COMP%] {\n  overflow: visible;\n}\n\n.grid[_ngcontent-%COMP%] {\n  position: sticky;\n  top: 0;\n  align-self: start;\n}\n\n.info-closed[_ngcontent-%COMP%] {\n  width: calc(100% - 2rem);\n}\n\n.info-open[_ngcontent-%COMP%] {\n  width: calc(100% - 20rem);\n}\n\n.info-disabled[_ngcontent-%COMP%] {\n  width: 100%;\n}\n\n.step-body[_ngcontent-%COMP%]:not(.grid) {\n  border-radius: 12px;\n  border: 1px solid #EAECF0;\n  box-shadow: 0 1px 2px 0 rgba(16, 24, 40, 0.06), 0 1px 3px 0 rgba(16, 24, 40, 0.1);\n}\n.step-body[_ngcontent-%COMP%]:not(.grid)   theia-dynamic-form[_ngcontent-%COMP%] {\n  padding: 1.5rem 1.5rem;\n  display: block;\n  overflow: auto;\n}\n\n.step-header[_ngcontent-%COMP%] {\n  border-bottom: 1px solid #EAECF0;\n}\n\n.step-footer[_ngcontent-%COMP%] {\n  padding: 1.5rem 1rem;\n  border-top: 1px solid #EAECF0;\n  display: flex;\n  flex-wrap: wrap;\n}\n\n.breadcrumbs[_ngcontent-%COMP%] {\n  display: flex;\n  align-items: center;\n  gap: 0.5rem;\n}\n.breadcrumbs[_ngcontent-%COMP%]   div[_ngcontent-%COMP%] {\n  color: #344054;\n  background-color: #F9FAFB;\n  padding: 0 0.5rem;\n}\n\nh3[_ngcontent-%COMP%] {\n  margin-bottom: 0;\n}\n\n.resizer[_ngcontent-%COMP%] {\n  width: 3px;\n  padding: 0;\n  position: absolute;\n  height: 100%;\n  left: calc(50% - 1px);\n  cursor: col-resize;\n  background-color: transparent;\n  z-index: 10000;\n}\n.resizer[_ngcontent-%COMP%]   i[_ngcontent-%COMP%] {\n  position: relative;\n  left: -5px;\n  top: calc(50% - 8px);\n  color: #D0D5DD;\n}\n.resizer[_ngcontent-%COMP%]:hover {\n  background-color: #96C0E0;\n}\n\n.json[_ngcontent-%COMP%] {\n  overflow: auto;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy9zdGVwcy9zdGVwcy5jb21wb25lbnQuc2NzcyIsIndlYnBhY2s6Ly8uL3NyYy9fZ2xvYmFscy5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUVBO0VBQ0UsaUJBQUE7QUFERjs7QUFJQTtFQUNFLGdCQUFBO0VBQ0EsTUFBQTtFQUNBLGlCQUFBO0FBREY7O0FBUUE7RUFDRSx3QkFBQTtBQUxGOztBQVFBO0VBQ0UseUJBQUE7QUFMRjs7QUFRQTtFQUNFLFdBQUE7QUFMRjs7QUFRQTtFQUNFLG1CQUFBO0VBQ0EseUJBQUE7RUFDQSxpRkFBQTtBQUxGO0FBTUU7RUFDRSxzQkFBQTtFQUNBLGNBQUE7RUFDQSxjQUFBO0FBSko7O0FBUUE7RUFDRSxnQ0FBQTtBQUxGOztBQVFBO0VBQ0Usb0JBQUE7RUFDQSw2QkFBQTtFQUNBLGFBQUE7RUFDQSxlQUFBO0FBTEY7O0FBUUE7RUFDRSxhQUFBO0VBQ0EsbUJBQUE7RUFDQSxXQUFBO0FBTEY7QUFPRTtFQUNFLGNDMUNPO0VEMkNQLHlCQ2hETTtFRGlETixpQkFBQTtBQUxKOztBQVNBO0VBQ0UsZ0JBQUE7QUFORjs7QUFTQTtFQUNFLFVBQUE7RUFDQSxVQUFBO0VBQ0Esa0JBQUE7RUFDQSxZQUFBO0VBQ0EscUJBQUE7RUFDQSxrQkFBQTtFQUNBLDZCQUFBO0VBQ0EsY0FBQTtBQU5GO0FBUUU7RUFDRSxrQkFBQTtFQUNBLFVBQUE7RUFDQSxvQkFBQTtFQUNBLGNDcEVPO0FEOERYO0FBVUU7RUFDRSx5QkNqRlU7QUR5RWQ7O0FBWUE7RUFDRSxjQUFBO0FBVEYiLCJzb3VyY2VzQ29udGVudCI6WyJAdXNlIFwiLi4vLi4vLi4vZ2xvYmFsc1wiO1xuXG5wcmUge1xuICBvdmVyZmxvdzogdmlzaWJsZTtcbn1cblxuLmdyaWQge1xuICBwb3NpdGlvbjogc3RpY2t5O1xuICB0b3A6IDA7XG4gIGFsaWduLXNlbGY6IHN0YXJ0O1xufVxuXG5cbjpob3N0IHtcblxufVxuLmluZm8tY2xvc2VkIHtcbiAgd2lkdGg6IGNhbGMoMTAwJSAtIDJyZW0pO1xufVxuXG4uaW5mby1vcGVuIHtcbiAgd2lkdGg6IGNhbGMoMTAwJSAtIDIwcmVtKTtcbn1cblxuLmluZm8tZGlzYWJsZWQge1xuICB3aWR0aDogMTAwJTtcbn1cblxuLnN0ZXAtYm9keTpub3QoLmdyaWQpIHtcbiAgYm9yZGVyLXJhZGl1czogMTJweDtcbiAgYm9yZGVyOiAxcHggc29saWQgZ2xvYmFscy4kZ3JheS0yMDA7XG4gIGJveC1zaGFkb3c6IDAgMXB4IDJweCAwIHJnYmEoMTYsIDI0LCA0MCwgMC4wNiksIDAgMXB4IDNweCAwIHJnYmEoMTYsIDI0LCA0MCwgMC4xMCk7XG4gIHRoZWlhLWR5bmFtaWMtZm9ybSB7XG4gICAgcGFkZGluZzogMS41cmVtIDEuNXJlbTtcbiAgICBkaXNwbGF5OiBibG9jaztcbiAgICBvdmVyZmxvdzogYXV0bztcbiAgfVxufVxuXG4uc3RlcC1oZWFkZXIge1xuICBib3JkZXItYm90dG9tOiAxcHggc29saWQgZ2xvYmFscy4kZ3JheS0yMDA7XG59XG5cbi5zdGVwLWZvb3RlciB7XG4gIHBhZGRpbmc6IDEuNXJlbSAxcmVtO1xuICBib3JkZXItdG9wOiAxcHggc29saWQgZ2xvYmFscy4kZ3JheS0yMDA7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXgtd3JhcDogd3JhcDtcbn1cblxuLmJyZWFkY3J1bWJzIHtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAgZ2FwOiAuNXJlbTtcblxuICBkaXYge1xuICAgIGNvbG9yOiBnbG9iYWxzLiRncmF5LTcwMDtcbiAgICBiYWNrZ3JvdW5kLWNvbG9yOiBnbG9iYWxzLiRncmF5LTUwO1xuICAgIHBhZGRpbmc6IDAgLjVyZW07XG4gIH1cbn1cblxuaDMge1xuICBtYXJnaW4tYm90dG9tOiAwO1xufVxuXG4ucmVzaXplciB7XG4gIHdpZHRoOiAzcHg7XG4gIHBhZGRpbmc6IDA7XG4gIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgaGVpZ2h0OiAxMDAlO1xuICBsZWZ0OiBjYWxjKDUwJSAtIDFweCk7XG4gIGN1cnNvcjogY29sLXJlc2l6ZTtcbiAgYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7XG4gIHotaW5kZXg6IDEwMDAwO1xuXG4gIGkge1xuICAgIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgICBsZWZ0OiAtNXB4O1xuICAgIHRvcDogY2FsYyg1MCUgLSA4cHgpO1xuICAgIGNvbG9yOiBnbG9iYWxzLiRncmF5LTMwMDtcbiAgfVxuXG5cbiAgJjpob3ZlciB7XG4gICAgYmFja2dyb3VuZC1jb2xvcjogZ2xvYmFscy4kcHJpbWFyeS0yMDA7XG4gIH1cbn1cblxuLmpzb24ge1xuICBvdmVyZmxvdzogYXV0bztcbn1cbiIsIiRmb250LWZhbWlseS1iYXNlOiBJbnRlciwgc2Fucy1zZXJpZjtcbiRoZWFkZXItaGVpZ2h0OiA0LjVyZW07XG4kZm9vdGVyLWhlaWdodDogNS41cmVtO1xuXG4kcHJpbWFyeS0yMDA6ICM5NkMwRTA7XG4kcHJpbWFyeS01MDA6ICMxQjc1QkI7XG4kcHJpbWFyeS02MDA6ICMxOTZBQUE7XG4kcHJpbWFyeS03MDA6ICMxMzUzODU7XG5cbiRncmF5LTUwOiAjRjlGQUZCO1xuJGdyYXktMTAwOiAjRjJGNEY3O1xuJGdyYXktMjAwOiAjRUFFQ0YwO1xuJGdyYXktMzAwOiAjRDBENUREO1xuJGdyYXktNjAwOiAjNDc1NDY3O1xuJGdyYXktNzAwOiAjMzQ0MDU0O1xuJGdyYXktODAwOiAjMUQyOTM5O1xuJGdyYXktOTAwOiAjMTAxODI4O1xuXG5cbiRsaW5rLWNvbG9yOiAkcHJpbWFyeS01MDAgIWRlZmF1bHQ7XG5cbkBtaXhpbiBoaWRlLXNjcm9sbGJhcnMge1xuICBzY3JvbGxiYXItd2lkdGg6IG5vbmU7XG4gIC1tcy1vdmVyZmxvdy1zdHlsZTogbm9uZTtcbiAgJjo6LXdlYmtpdC1zY3JvbGxiYXIge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cbn1cbiJdLCJzb3VyY2VSb290IjoiIn0= */"]
    });
  }
  return StepsComponent;
})();

/***/ }),

/***/ 7354:
/*!*********************************************************!*\
  !*** ./src/app/components/tab-bar/tab-bar.component.ts ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TabBarComponent: () => (/* binding */ TabBarComponent)
/* harmony export */ });
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../models/template */ 5339);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_template_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../services/template.service */ 529);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ 7947);





const _c0 = function (a0, a1) {
  return [a0, a1];
};
function TabBarComponent_li_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "li", 3)(1, "a", 4);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](2);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const section_r1 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("routerLink", _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpureFunction2"](2, _c0, section_r1.static ? "" : "/action", section_r1.route));
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtextInterpolate"](section_r1.label);
  }
}
let TabBarComponent = /*#__PURE__*/(() => {
  class TabBarComponent {
    constructor(templateService) {
      this.templateService = templateService;
      this.TheiaType = _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaType;
      this.template$ = templateService.template$;
    }
    static #_ = this.ɵfac = function TabBarComponent_Factory(t) {
      return new (t || TabBarComponent)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_template_service__WEBPACK_IMPORTED_MODULE_2__.TemplateService));
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: TabBarComponent,
      selectors: [["theia-tab-bar"]],
      decls: 4,
      vars: 3,
      consts: [[1, "card-header"], [1, "nav", "nav-tabs", "card-header-tabs"], ["class", "nav-item", 4, "ngFor", "ngForOf"], [1, "nav-item"], ["routerLinkActive", "active", 1, "nav-link", 3, "routerLink"]],
      template: function TabBarComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 0)(1, "ul", 1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtemplate"](2, TabBarComponent_li_2_Template, 3, 5, "li", 2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipe"](3, "async");
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()();
        }
        if (rf & 2) {
          let tmp_0_0;
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngForOf", (tmp_0_0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵpipeBind1"](3, 1, ctx.template$)) == null ? null : tmp_0_0.sections);
        }
      },
      dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_3__.NgForOf, _angular_router__WEBPACK_IMPORTED_MODULE_4__.RouterLink, _angular_router__WEBPACK_IMPORTED_MODULE_4__.RouterLinkActive, _angular_common__WEBPACK_IMPORTED_MODULE_3__.AsyncPipe],
      styles: ["/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return TabBarComponent;
})();

/***/ }),

/***/ 3858:
/*!***************************************************************!*\
  !*** ./src/app/components/type-ahead/type-ahead.component.ts ***!
  \***************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TypeAheadComponent: () => (/* binding */ TypeAheadComponent)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ 655);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ 9736);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ 3317);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ 4520);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ 9016);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/forms */ 8849);





const _c0 = ["input"];
let TypeAheadComponent = /*#__PURE__*/(() => {
  class TypeAheadComponent {
    constructor() {
      this.minLength = 3;
      this.valueChange = new _angular_core__WEBPACK_IMPORTED_MODULE_0__.EventEmitter();
    }
    ngAfterViewInit() {
      this.buttonSubscription$ = (0,rxjs__WEBPACK_IMPORTED_MODULE_1__.fromEvent)(this.input.nativeElement, 'input').pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_2__.debounceTime)(200), (0,rxjs_operators__WEBPACK_IMPORTED_MODULE_3__.map)(event => event.target?.value), (0,rxjs_operators__WEBPACK_IMPORTED_MODULE_4__.distinctUntilChanged)(), (0,rxjs_operators__WEBPACK_IMPORTED_MODULE_5__.filter)(value => value?.length === 0 || value?.length >= this.minLength)).subscribe(event => {
        this.valueChange.emit(event);
      });
    }
    ngOnDestroy() {
      this.buttonSubscription$?.unsubscribe();
    }
    static #_ = this.ɵfac = function TypeAheadComponent_Factory(t) {
      return new (t || TypeAheadComponent)();
    };
    static #_2 = this.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
      type: TypeAheadComponent,
      selectors: [["theia-type-ahead"]],
      viewQuery: function TypeAheadComponent_Query(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵviewQuery"](_c0, 7);
        }
        if (rf & 2) {
          let _t;
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.input = _t.first);
        }
      },
      inputs: {
        value: "value",
        placeHolder: "placeHolder",
        minLength: "minLength"
      },
      outputs: {
        valueChange: "valueChange"
      },
      decls: 4,
      vars: 2,
      consts: [["xmlns", "http://www.w3.org/2000/svg", "width", "20", "height", "20", "viewBox", "0 0 20 20", "fill", "none"], ["d", "M17.5 17.5L14.5834 14.5833M16.6667 9.58333C16.6667 13.4954 13.4954 16.6667 9.58333 16.6667C5.67132 16.6667 2.5 13.4954 2.5 9.58333C2.5 5.67132 5.67132 2.5 9.58333 2.5C13.4954 2.5 16.6667 5.67132 16.6667 9.58333Z", "stroke", "#667085", "stroke-width", "1.66667", "stroke-linecap", "round", "stroke-linejoin", "round"], ["type", "search", 1, "form-control", 3, "ngModel", "placeholder", "ngModelChange"], ["input", ""]],
      template: function TypeAheadComponent_Template(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "svg", 0);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "path", 1);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceHTML"]();
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "input", 2, 3);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("ngModelChange", function TypeAheadComponent_Template_input_ngModelChange_2_listener($event) {
            return ctx.value = $event;
          });
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        }
        if (rf & 2) {
          let tmp_1_0;
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](2);
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("ngModel", ctx.value)("placeholder", (tmp_1_0 = ctx.placeHolder) !== null && tmp_1_0 !== undefined ? tmp_1_0 : "Search...");
        }
      },
      dependencies: [_angular_forms__WEBPACK_IMPORTED_MODULE_6__.DefaultValueAccessor, _angular_forms__WEBPACK_IMPORTED_MODULE_6__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_6__.NgModel],
      styles: ["[_nghost-%COMP%] {\n  position: relative;\n}\n[_nghost-%COMP%]   svg[_ngcontent-%COMP%] {\n  position: absolute;\n  pointer-events: none;\n  left: 0.75rem;\n  top: 0.75rem;\n}\n[_nghost-%COMP%]   input[_ngcontent-%COMP%] {\n  padding-left: 2.75rem;\n  height: 2.75rem;\n}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3NyYy9hcHAvY29tcG9uZW50cy90eXBlLWFoZWFkL3R5cGUtYWhlYWQuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxrQkFBQTtBQUNGO0FBQ0U7RUFDRSxrQkFBQTtFQUNBLG9CQUFBO0VBQ0EsYUFBQTtFQUNBLFlBQUE7QUFDSjtBQUNFO0VBQ0UscUJBQUE7RUFDQSxlQUFBO0FBQ0oiLCJzb3VyY2VzQ29udGVudCI6WyI6aG9zdCB7XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcblxuICBzdmcge1xuICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgICBwb2ludGVyLWV2ZW50czogbm9uZTtcbiAgICBsZWZ0OiAwLjc1cmVtO1xuICAgIHRvcDogMC43NXJlbTtcbiAgfVxuICBpbnB1dCB7XG4gICAgcGFkZGluZy1sZWZ0OiAyLjc1cmVtO1xuICAgIGhlaWdodDogMi43NXJlbTtcbiAgfVxufVxuIl0sInNvdXJjZVJvb3QiOiIifQ== */"]
    });
  }
  return TypeAheadComponent;
})();

/***/ }),

/***/ 2432:
/*!************************************************************!*\
  !*** ./src/app/directives/control-attributes.directive.ts ***!
  \************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ControlAttributesDirective: () => (/* binding */ ControlAttributesDirective)
/* harmony export */ });
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../models/template */ 5339);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 1699);


let ControlAttributesDirective = /*#__PURE__*/(() => {
  class ControlAttributesDirective {
    constructor(el) {
      this.el = el;
      this.theiaControlAttributes = {
        type: _models_template__WEBPACK_IMPORTED_MODULE_0__.TheiaType.Attributes
      };
    }
    ngAfterViewInit() {
      for (const [key, value] of Object.entries(this.theiaControlAttributes || {})) {
        if (key === 'type') {
          return;
        }
        this.el.nativeElement.setAttribute(key, value);
      }
    }
    static #_ = this.ɵfac = function ControlAttributesDirective_Factory(t) {
      return new (t || ControlAttributesDirective)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_1__.ElementRef));
    };
    static #_2 = this.ɵdir = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineDirective"]({
      type: ControlAttributesDirective,
      selectors: [["", "theiaControlAttributes", ""]],
      inputs: {
        theiaControlAttributes: "theiaControlAttributes"
      }
    });
  }
  return ControlAttributesDirective;
})();

/***/ }),

/***/ 1501:
/*!**************************************************!*\
  !*** ./src/app/directives/dropdown.directive.ts ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DropdownDirective: () => (/* binding */ DropdownDirective)
/* harmony export */ });
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);


let DropdownDirective = /*#__PURE__*/(() => {
  class DropdownDirective {
    constructor(eRef, document) {
      this.eRef = eRef;
      this.document = document;
      this.visible = false;
    }
    onClick(event) {
      event.preventDefault();
      this.visible = !this.visible;
      this.updateDropdown();
    }
    clickOut(event) {
      const link = this.eRef.nativeElement;
      if (!link.contains(event.target)) {
        this.visible = false;
        this.updateDropdown();
      }
    }
    updateDropdown() {
      const dropdown = this.eRef.nativeElement.nextSibling;
      if (this.visible) {
        dropdown.classList.add('show');
        const rect = dropdown.getBoundingClientRect();
        const width = this.document.documentElement.clientWidth;
        if (rect.right > width) {
          dropdown.style.left = `${width - rect.right - 16}px`;
        }
      } else {
        dropdown.classList.remove('show');
      }
    }
    static #_ = this.ɵfac = function DropdownDirective_Factory(t) {
      return new (t || DropdownDirective)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.ElementRef), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_common__WEBPACK_IMPORTED_MODULE_1__.DOCUMENT));
    };
    static #_2 = this.ɵdir = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineDirective"]({
      type: DropdownDirective,
      selectors: [["", "theiaDropdown", ""]],
      hostBindings: function DropdownDirective_HostBindings(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("click", function DropdownDirective_click_HostBindingHandler($event) {
            return ctx.onClick($event);
          })("click", function DropdownDirective_click_HostBindingHandler($event) {
            return ctx.clickOut($event);
          }, false, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵresolveDocument"]);
        }
      }
    });
  }
  return DropdownDirective;
})();

/***/ }),

/***/ 30:
/*!****************************************************!*\
  !*** ./src/app/directives/log-stream.directive.ts ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   LogStreamDirective: () => (/* binding */ LogStreamDirective)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_sse_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../services/sse.service */ 8554);


let LogStreamDirective = /*#__PURE__*/(() => {
  class LogStreamDirective {
    constructor(sse, renderer, element) {
      this.sse = sse;
      this.renderer = renderer;
      this.element = element;
    }
    ngAfterViewInit() {
      if (!this.dataSource) {
        throw new Error('Datasource not defined');
      }
      this.eventSource$ = this.sse.createEventSource(this.dataSource).subscribe(this.handleLogEvent.bind(this));
    }
    ngOnDestroy() {
      this.eventSource$?.unsubscribe();
    }
    handleLogEvent(log) {
      const container = this.renderer.createElement("div");
      const text = this.renderer.createText(log);
      this.renderer.appendChild(container, text);
      this.renderer.appendChild(this.element.nativeElement, container);
    }
    static #_ = this.ɵfac = function LogStreamDirective_Factory(t) {
      return new (t || LogStreamDirective)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_services_sse_service__WEBPACK_IMPORTED_MODULE_1__.SSEService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.Renderer2), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.ElementRef));
    };
    static #_2 = this.ɵdir = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineDirective"]({
      type: LogStreamDirective,
      selectors: [["", "theiaLogStream", "", "dataSource", ""]],
      inputs: {
        dataSource: "dataSource"
      }
    });
  }
  return LogStreamDirective;
})();

/***/ }),

/***/ 5067:
/*!*********************************************************!*\
  !*** ./src/app/directives/resize-observer.directive.ts ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ResizeObserverDirective: () => (/* binding */ ResizeObserverDirective)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);


let ResizeObserverDirective = /*#__PURE__*/(() => {
  class ResizeObserverDirective {
    constructor(host, zone) {
      this.host = host;
      this.zone = zone;
      this.resize = new _angular_core__WEBPACK_IMPORTED_MODULE_0__.EventEmitter();
    }
    ngOnInit() {
      this.observer = new ResizeObserver(this.handleResize.bind(this));
      this.observer.observe(this.host.nativeElement);
    }
    ngOnDestroy() {
      this.observer?.unobserve(this.host.nativeElement);
    }
    handleResize([entry]) {
      this.zone.run(() => {
        this.resize.emit(entry.contentRect);
      });
    }
    static #_ = this.ɵfac = function ResizeObserverDirective_Factory(t) {
      return new (t || ResizeObserverDirective)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.ElementRef), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.NgZone));
    };
    static #_2 = this.ɵdir = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineDirective"]({
      type: ResizeObserverDirective,
      selectors: [["", "theiaResizeObserver", ""]],
      outputs: {
        resize: "resize"
      }
    });
  }
  return ResizeObserverDirective;
})();

/***/ }),

/***/ 7637:
/*!*******************************************************!*\
  !*** ./src/app/directives/static-action.directive.ts ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   StaticActionDirective: () => (/* binding */ StaticActionDirective)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);

let StaticActionDirective = /*#__PURE__*/(() => {
  class StaticActionDirective {
    constructor(viewContainerRef) {
      this.viewContainerRef = viewContainerRef;
    }
    static #_ = this.ɵfac = function StaticActionDirective_Factory(t) {
      return new (t || StaticActionDirective)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.ViewContainerRef));
    };
    static #_2 = this.ɵdir = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineDirective"]({
      type: StaticActionDirective,
      selectors: [["", "theiaStaticAction", ""]]
    });
  }
  return StaticActionDirective;
})();

/***/ }),

/***/ 8520:
/*!*************************************************!*\
  !*** ./src/app/directives/submenu.directive.ts ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SubmenuDirective: () => (/* binding */ SubmenuDirective)
/* harmony export */ });
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);


let SubmenuDirective = /*#__PURE__*/(() => {
  class SubmenuDirective {
    constructor(eRef, document) {
      this.eRef = eRef;
      this.document = document;
      this.visible = false;
    }
    onMouseEnter(event) {
      event.preventDefault();
      this.visible = true;
      this.updateSubmenu();
    }
    onMouseLeave(event) {
      event.preventDefault();
      this.visible = false;
      this.updateSubmenu();
    }
    updateSubmenu() {
      const dropdown = this.eRef.nativeElement.querySelector('.submenu');
      const rect = this.eRef.nativeElement.getBoundingClientRect();
      if (this.visible) {
        Object.assign(dropdown.style, {
          left: `${rect.x + rect.width}px`,
          top: `${rect.y - 9}px`
        });
        dropdown.classList.add('show');
      } else {
        dropdown.classList.remove('show');
      }
    }
    static #_ = this.ɵfac = function SubmenuDirective_Factory(t) {
      return new (t || SubmenuDirective)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_core__WEBPACK_IMPORTED_MODULE_0__.ElementRef), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_angular_common__WEBPACK_IMPORTED_MODULE_1__.DOCUMENT));
    };
    static #_2 = this.ɵdir = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineDirective"]({
      type: SubmenuDirective,
      selectors: [["", "theiaSubmenu", ""]],
      hostBindings: function SubmenuDirective_HostBindings(rf, ctx) {
        if (rf & 1) {
          _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵlistener"]("mouseenter", function SubmenuDirective_mouseenter_HostBindingHandler($event) {
            return ctx.onMouseEnter($event);
          })("mouseleave", function SubmenuDirective_mouseleave_HostBindingHandler($event) {
            return ctx.onMouseLeave($event);
          });
        }
      }
    });
  }
  return SubmenuDirective;
})();

/***/ }),

/***/ 2985:
/*!***************************************************!*\
  !*** ./src/app/interceptors/cloud.interceptor.ts ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CloudInterceptor: () => (/* binding */ CloudInterceptor)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_cloud_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../services/cloud.service */ 9509);
/* harmony import */ var _services_allowed_apps_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../services/allowed-apps.service */ 9726);



let CloudInterceptor = /*#__PURE__*/(() => {
  class CloudInterceptor {
    constructor(cloud, app) {
      this.cloud = cloud;
      this.app = app;
    }
    intercept(request, next) {
      const params = request.params.set('cloud', this.cloud.getSelectedCloud().value).set('rc_app_context', this.app.getSelectedApp().value);
      return next.handle(request.clone({
        params
      }));
    }
    static #_ = this.ɵfac = function CloudInterceptor_Factory(t) {
      return new (t || CloudInterceptor)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](_services_cloud_service__WEBPACK_IMPORTED_MODULE_1__.CloudService), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](_services_allowed_apps_service__WEBPACK_IMPORTED_MODULE_2__.AllowedAppsService));
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjectable"]({
      token: CloudInterceptor,
      factory: CloudInterceptor.ɵfac
    });
  }
  return CloudInterceptor;
})();

/***/ }),

/***/ 1649:
/*!*************************************************************!*\
  !*** ./src/app/interceptors/template-reload.interceptor.ts ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TemplateReloadInterceptor: () => (/* binding */ TemplateReloadInterceptor)
/* harmony export */ });
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common/http */ 4860);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ 4980);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! rxjs/operators */ 2607);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ 9736);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _services_template_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../services/template.service */ 529);





let TemplateReloadInterceptor = /*#__PURE__*/(() => {
  class TemplateReloadInterceptor {
    constructor(templateService) {
      this.templateService = templateService;
    }
    intercept(request, next) {
      return next.handle(request).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_0__.mergeMap)(event => {
        if (event instanceof _angular_common_http__WEBPACK_IMPORTED_MODULE_1__.HttpResponse && event.headers.has('RapidCloud-Force-Template-Reload')) {
          return this.templateService.getTemplate().pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_2__.map)(() => event));
        } else {
          return (0,rxjs__WEBPACK_IMPORTED_MODULE_3__.of)(event);
        }
      }));
    }
    static #_ = this.ɵfac = function TemplateReloadInterceptor_Factory(t) {
      return new (t || TemplateReloadInterceptor)(_angular_core__WEBPACK_IMPORTED_MODULE_4__["ɵɵinject"](_services_template_service__WEBPACK_IMPORTED_MODULE_5__.TemplateService));
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_4__["ɵɵdefineInjectable"]({
      token: TemplateReloadInterceptor,
      factory: TemplateReloadInterceptor.ɵfac
    });
  }
  return TemplateReloadInterceptor;
})();

/***/ }),

/***/ 1708:
/*!********************************!*\
  !*** ./src/app/models/grid.ts ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SortOrder: () => (/* binding */ SortOrder)
/* harmony export */ });
var SortOrder = /*#__PURE__*/function (SortOrder) {
  SortOrder[SortOrder["Asc"] = 0] = "Asc";
  SortOrder[SortOrder["Desc"] = 1] = "Desc";
  return SortOrder;
}(SortOrder || {});

/***/ }),

/***/ 6347:
/*!********************************************!*\
  !*** ./src/app/models/template/control.ts ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   hasDatasource: () => (/* binding */ hasDatasource),
/* harmony export */   isCodeControl: () => (/* binding */ isCodeControl),
/* harmony export */   isComplexControl: () => (/* binding */ isComplexControl),
/* harmony export */   isCompositeGroupControl: () => (/* binding */ isCompositeGroupControl),
/* harmony export */   isCompositeModuleControl: () => (/* binding */ isCompositeModuleControl),
/* harmony export */   isInputControl: () => (/* binding */ isInputControl),
/* harmony export */   isKeyValueControl: () => (/* binding */ isKeyValueControl),
/* harmony export */   isMultiSelectControl: () => (/* binding */ isMultiSelectControl),
/* harmony export */   isSelectControl: () => (/* binding */ isSelectControl),
/* harmony export */   isSelectOrMultiSelect: () => (/* binding */ isSelectOrMultiSelect),
/* harmony export */   isTextAreaControl: () => (/* binding */ isTextAreaControl),
/* harmony export */   isToggleControl: () => (/* binding */ isToggleControl),
/* harmony export */   isUploadControl: () => (/* binding */ isUploadControl)
/* harmony export */ });
/* harmony import */ var _theia_control__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./theia-control */ 7044);

function isInputControl(control) {
  return control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.Input;
}
function isKeyValueControl(control) {
  return control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.KeyValue;
}
function isToggleControl(control) {
  return control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.Toggle;
}
function isSelectControl(control) {
  return control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.Select;
}
function isMultiSelectControl(control) {
  return control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.MultiSelect;
}
function isTextAreaControl(control) {
  return control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.TextArea;
}
function isCodeControl(control) {
  return control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.Code;
}
function isUploadControl(control) {
  return control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.Upload;
}
function isCompositeModuleControl(control) {
  return control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.CompositeModule;
}
function isCompositeGroupControl(control) {
  return control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.CompositeGroup;
}
function isComplexControl(control) {
  return control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.KeyValue || control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.CompositeModule || control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.Code || control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.Upload || control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.CompositeGroup;
}
function hasDatasource(control) {
  return control && control.type !== _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.CompositeModule && control.type !== _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.CompositeGroup;
}
function isSelectOrMultiSelect(control) {
  return control && (control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.Select || control.type === _theia_control__WEBPACK_IMPORTED_MODULE_0__.TheiaControl.MultiSelect);
}

/***/ }),

/***/ 1657:
/*!**********************************************!*\
  !*** ./src/app/models/template/dashboard.ts ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PanelType: () => (/* binding */ PanelType)
/* harmony export */ });
var PanelType = /*#__PURE__*/function (PanelType) {
  PanelType["Markdown"] = "Theia::Panel::Markdown";
  PanelType["Table"] = "Theia::Panel::Table";
  return PanelType;
}(PanelType || {});

/***/ }),

/***/ 7044:
/*!**************************************************!*\
  !*** ./src/app/models/template/theia-control.ts ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TheiaControl: () => (/* binding */ TheiaControl)
/* harmony export */ });
var TheiaControl = /*#__PURE__*/function (TheiaControl) {
  TheiaControl["Input"] = "Theia::Control::Input";
  TheiaControl["Select"] = "Theia::Control::Select";
  TheiaControl["Toggle"] = "Theia::Control::Toggle";
  TheiaControl["MultiSelect"] = "Theia::Control::MultiSelect";
  TheiaControl["KeyValue"] = "Theia::Control::KeyValue";
  TheiaControl["TextArea"] = "Theia::Control::TextArea";
  TheiaControl["CompositeModule"] = "Theia::Control::CompositeModule";
  TheiaControl["Code"] = "Theia::Control::Code";
  TheiaControl["Upload"] = "Theia::Control::Upload";
  TheiaControl["CompositeGroup"] = "Theia::Control::CompositeGroup";
  return TheiaControl;
}(TheiaControl || {});

/***/ }),

/***/ 9671:
/*!***********************************************!*\
  !*** ./src/app/models/template/theia-step.ts ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TheiaStep: () => (/* binding */ TheiaStep)
/* harmony export */ });
var TheiaStep = /*#__PURE__*/function (TheiaStep) {
  TheiaStep["Grid"] = "Theia::Step::Grid";
  TheiaStep["Form"] = "Theia::Step::Form";
  TheiaStep["Json"] = "Theia::Step::Json";
  TheiaStep["Log"] = "Theia::Step::Log";
  return TheiaStep;
}(TheiaStep || {});

/***/ }),

/***/ 5339:
/*!***********************************************!*\
  !*** ./src/app/models/template/theia-type.ts ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TheiaType: () => (/* binding */ TheiaType)
/* harmony export */ });
var TheiaType = /*#__PURE__*/function (TheiaType) {
  TheiaType["Template"] = "Theia::Template";
  TheiaType["Section"] = "Theia::Section";
  TheiaType["Action"] = "Theia::Action";
  TheiaType["Step"] = "Theia::Step";
  TheiaType["Attributes"] = "Theia::Attribute";
  TheiaType["Control"] = "Theia::Control";
  TheiaType["Option"] = "Theia::Option";
  TheiaType["Validation"] = "Theia::Validation";
  TheiaType["DataOption"] = "Theia::DataOption";
  TheiaType["Dashboard"] = "Theia::Dashboard";
  return TheiaType;
}(TheiaType || {});

/***/ }),

/***/ 1249:
/*!*****************************************************!*\
  !*** ./src/app/models/template/theia-validation.ts ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TheiaValidation: () => (/* binding */ TheiaValidation)
/* harmony export */ });
var TheiaValidation = /*#__PURE__*/function (TheiaValidation) {
  TheiaValidation["Email"] = "Theia::Validation::Email";
  TheiaValidation["Max"] = "Theia::Validation::Max";
  TheiaValidation["Min"] = "Theia::Validation::Min";
  TheiaValidation["MinLength"] = "Theia::Validation::MinLength";
  TheiaValidation["MaxLength"] = "Theia::Validation::MaxLength";
  TheiaValidation["Pattern"] = "Theia::Validation::Pattern";
  TheiaValidation["Required"] = "Theia::Validation::Required";
  TheiaValidation["RequiredTrue"] = "Theia::Validation::RequiredTrue";
  return TheiaValidation;
}(TheiaValidation || {});

/***/ }),

/***/ 77:
/*!*****************************************!*\
  !*** ./src/app/pipes/file-size.pipe.ts ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FileSizePipe: () => (/* binding */ FileSizePipe)
/* harmony export */ });
/* harmony import */ var filesize__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! filesize */ 5726);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 1699);


let FileSizePipe = /*#__PURE__*/(() => {
  class FileSizePipe {
    transform(bytes) {
      return (0,filesize__WEBPACK_IMPORTED_MODULE_0__.filesize)(bytes);
    }
    static #_ = this.ɵfac = function FileSizePipe_Factory(t) {
      return new (t || FileSizePipe)();
    };
    static #_2 = this.ɵpipe = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefinePipe"]({
      name: "fileSize",
      type: FileSizePipe,
      pure: true
    });
  }
  return FileSizePipe;
})();

/***/ }),

/***/ 8475:
/*!*******************************************!*\
  !*** ./src/app/pipes/remove-null.pipe.ts ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   RemoveNullPipe: () => (/* binding */ RemoveNullPipe)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);

let RemoveNullPipe = /*#__PURE__*/(() => {
  class RemoveNullPipe {
    transform(value) {
      return this.removeEmpty(value);
    }
    removeEmpty(obj) {
      Object.keys(obj).forEach(key => {
        if (obj[key] && typeof obj[key] === 'object') {
          this.removeEmpty(obj[key]);
        } else if (obj[key] === undefined || obj[key] === null) {
          delete obj[key];
        }
      });
      return obj;
    }
    static #_ = this.ɵfac = function RemoveNullPipe_Factory(t) {
      return new (t || RemoveNullPipe)();
    };
    static #_2 = this.ɵpipe = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefinePipe"]({
      name: "removeNull",
      type: RemoveNullPipe,
      pure: true
    });
  }
  return RemoveNullPipe;
})();

/***/ }),

/***/ 9726:
/*!**************************************************!*\
  !*** ./src/app/services/allowed-apps.service.ts ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AllowedAppsService: () => (/* binding */ AllowedAppsService)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ 8071);
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../environments/environment */ 553);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ 3738);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ 4860);
/* harmony import */ var _local_storage_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./local-storage.service */ 3683);






let AllowedAppsService = /*#__PURE__*/(() => {
  class AllowedAppsService {
    constructor(http, localStorageService) {
      this.http = http;
      this.localStorageService = localStorageService;
      this.allowedApps$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject({});
      this.selectedApp$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject("");
    }
    getAllowedApps() {
      return this.http.get(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/allowed_apps`).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_2__.tap)(response => {
        this.allowedApps$.next(response);
      }));
    }
    getSelectedApp() {
      if (!this.selectedApp$.getValue()) {
        const selectedApp = this.localStorageService.getItem('selectedApp');
        if (selectedApp) {
          this.selectedApp$.next(selectedApp);
        } else {
          this.setSelectedApp('aws');
        }
      }
      return this.selectedApp$;
    }
    setSelectedApp(value) {
      this.selectedApp$.next(value);
      this.localStorageService.setItem('selectedApp', value);
    }
    static #_ = this.ɵfac = function AllowedAppsService_Factory(t) {
      return new (t || AllowedAppsService)(_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_4__.HttpClient), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵinject"](_local_storage_service__WEBPACK_IMPORTED_MODULE_5__.LocalStorageService));
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdefineInjectable"]({
      token: AllowedAppsService,
      factory: AllowedAppsService.ɵfac,
      providedIn: 'root'
    });
  }
  return AllowedAppsService;
})();

/***/ }),

/***/ 9509:
/*!*******************************************!*\
  !*** ./src/app/services/cloud.service.ts ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CloudService: () => (/* binding */ CloudService)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ 8071);
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../environments/environment */ 553);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ 3738);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ 4860);
/* harmony import */ var _local_storage_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./local-storage.service */ 3683);






let CloudService = /*#__PURE__*/(() => {
  class CloudService {
    constructor(http, localStorageService) {
      this.http = http;
      this.localStorageService = localStorageService;
      this.availableClouds$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject({
        aws: {
          cloud_label: "AWS",
          account_label: "Account",
          region_label: "Region",
          vpc_label: "VPC"
        }
      });
      this.selectedCloud$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject("");
    }
    getClouds() {
      return this.http.get(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/clouds`).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_2__.tap)(response => {
        this.availableClouds$.next(response);
      }));
    }
    getSelectedCloud() {
      if (!this.selectedCloud$.getValue()) {
        const selectedCloud = this.localStorageService.getItem('selectedCloud');
        if (selectedCloud) {
          this.selectedCloud$.next(selectedCloud);
        } else {
          this.setSelectedCloud('aws');
        }
      }
      return this.selectedCloud$;
    }
    setSelectedCloud(value) {
      this.selectedCloud$.next(value);
      this.localStorageService.setItem('selectedCloud', value);
    }
    static #_ = this.ɵfac = function CloudService_Factory(t) {
      return new (t || CloudService)(_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_4__.HttpClient), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵinject"](_local_storage_service__WEBPACK_IMPORTED_MODULE_5__.LocalStorageService));
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdefineInjectable"]({
      token: CloudService,
      factory: CloudService.ɵfac,
      providedIn: 'root'
    });
  }
  return CloudService;
})();

/***/ }),

/***/ 9167:
/*!*********************************************!*\
  !*** ./src/app/services/command.service.ts ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CommandService: () => (/* binding */ CommandService)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ 8071);
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../environments/environment */ 553);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common/http */ 4860);
/* harmony import */ var _environment_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./environment.service */ 1574);





let CommandService = /*#__PURE__*/(() => {
  class CommandService {
    constructor(http, env) {
      this.http = http;
      this.env = env;
      this.isNew$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject(false);
    }
    get isNew() {
      return this.isNew$.value;
    }
    set isNew(value) {
      this.isNew$.next(value);
    }
    runCommand(payload) {
      const env = this.env.getCurrentEnvironment().getValue();
      payload.env = env?.name;
      return this.http.post(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/command`, payload);
    }
    static #_ = this.ɵfac = function CommandService_Factory(t) {
      return new (t || CommandService)(_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_3__.HttpClient), _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵinject"](_environment_service__WEBPACK_IMPORTED_MODULE_4__.EnvironmentService));
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdefineInjectable"]({
      token: CommandService,
      factory: CommandService.ɵfac,
      providedIn: 'root'
    });
  }
  return CommandService;
})();

/***/ }),

/***/ 6678:
/*!*************************************************!*\
  !*** ./src/app/services/data-source.service.ts ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DataSourceService: () => (/* binding */ DataSourceService)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ 3252);
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../environments/environment */ 553);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common/http */ 4860);
/* harmony import */ var _environment_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./environment.service */ 1574);





let DataSourceService = /*#__PURE__*/(() => {
  class DataSourceService {
    constructor(http, environmentService) {
      this.http = http;
      this.environmentService = environmentService;
    }
    getData(endpoint = '', envRequired = false, params = {}) {
      const env = this.environmentService.getCurrentEnvironment().value?.name;
      if (envRequired && !env) {
        return (0,rxjs__WEBPACK_IMPORTED_MODULE_1__.throwError)("No environment selected");
      }
      let queryParams = envRequired ? `&env=${env}` : '';
      for (const [param, value] of Object.entries(params)) {
        queryParams += `&${param}=${value}`;
      }
      return this.http.get(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/${endpoint}${queryParams}`);
    }
    static #_ = this.ɵfac = function DataSourceService_Factory(t) {
      return new (t || DataSourceService)(_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_3__.HttpClient), _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵinject"](_environment_service__WEBPACK_IMPORTED_MODULE_4__.EnvironmentService));
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdefineInjectable"]({
      token: DataSourceService,
      factory: DataSourceService.ɵfac,
      providedIn: 'root'
    });
  }
  return DataSourceService;
})();

/***/ }),

/***/ 449:
/*!**************************************************!*\
  !*** ./src/app/services/dynamic-form.service.ts ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DynamicFormService: () => (/* binding */ DynamicFormService)
/* harmony export */ });
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../models/template */ 7044);
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../models/template */ 5339);
/* harmony import */ var _models_template_control__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../models/template/control */ 6347);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ 8849);
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../environments/environment */ 553);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ 3317);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs/operators */ 655);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! rxjs/operators */ 4520);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _window_ref_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./window-ref.service */ 6889);
/* harmony import */ var _command_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./command.service */ 9167);
/* harmony import */ var _data_source_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./data-source.service */ 6678);










let DynamicFormService = /*#__PURE__*/(() => {
  class DynamicFormService {
    constructor(fb, windowRef, commandService, dataSourceService) {
      this.fb = fb;
      this.windowRef = windowRef;
      this.commandService = commandService;
      this.dataSourceService = dataSourceService;
      this.window = windowRef.nativeWindow;
    }
    initialize(formGroup, controls, cdr, options) {
      const dependencyControls = [];
      const selectControls = [];
      const dynamicDatasourceControls = [];
      const addControls = controls => {
        controls?.forEach(control => {
          if (control.type === _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaControl.CompositeModule) {
            control.modules?.forEach(module => {
              this.addControl(module, formGroup, dependencyControls, selectControls, dynamicDatasourceControls);
              addControls(module.controls);
            });
            return;
          }
          this.addControl(control, formGroup, dependencyControls, selectControls, dynamicDatasourceControls);
        });
      };
      addControls(controls);
      this.initializeSelectControls(formGroup, selectControls, controls);
      this.initializeDependencyControls(formGroup, dependencyControls);
      this.initializeDynamicDatasourceControls(formGroup, dynamicDatasourceControls, controls);
      if (options.readonly && !this.commandService.isNew) {
        formGroup.disable();
      }
      if (options.datasource) {
        this.dataSourceService.getData(options.datasource, options.env_param_required).subscribe(([response]) => {
          Object.keys(formGroup.controls).forEach(key => {
            const control = formGroup.controls[key];
            if (control instanceof _angular_forms__WEBPACK_IMPORTED_MODULE_2__.FormArray) {
              formGroup.controls[key].setValue(response[key] || control.value);
            } else {
              formGroup.controls[key].setValue(response[key]);
            }
          });
        });
      }
    }
    addControl(control, formGroup, dependencyControls = [], selectControls = [], dynamicDatasourceControls = []) {
      const formControl = formGroup.get(control.id);
      if (formControl) {
        formControl.setValidators(this.getValidatorList(control));
        formControl.updateValueAndValidity();
      } else {
        if (control.type === _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaControl.CompositeGroup) {
          formGroup.addControl(control.id, new _angular_forms__WEBPACK_IMPORTED_MODULE_2__.UntypedFormArray([]));
        } else {
          formGroup.addControl(control.id, this.fb.control(control.default, this.getValidatorList(control)));
        }
      }
      if (!(0,_models_template_control__WEBPACK_IMPORTED_MODULE_3__.isComplexControl)(control) && control.dependency?.controlId) {
        dependencyControls.push(control);
      }
      if (control.type === _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaControl.Select) {
        selectControls.push(control);
      }
      if ((0,_models_template_control__WEBPACK_IMPORTED_MODULE_3__.hasDatasource)(control) && control.dynamic_datasource) {
        dynamicDatasourceControls.push(control);
      }
    }
    getValidatorList(control) {
      let result = [];
      if (!(0,_models_template_control__WEBPACK_IMPORTED_MODULE_3__.isComplexControl)(control)) {
        if (control.validations) {
          result = control.validations.reduce((prev, curr) => {
            const validationTypeMap = {
              'Theia::Validation::Email': _angular_forms__WEBPACK_IMPORTED_MODULE_2__.Validators.email,
              'Theia::Validation::Max': _angular_forms__WEBPACK_IMPORTED_MODULE_2__.Validators.max(Number(curr.value)),
              'Theia::Validation::Min': _angular_forms__WEBPACK_IMPORTED_MODULE_2__.Validators.min(Number(curr.value)),
              'Theia::Validation::MinLength': _angular_forms__WEBPACK_IMPORTED_MODULE_2__.Validators.minLength(Number(curr.value)),
              'Theia::Validation::MaxLength': _angular_forms__WEBPACK_IMPORTED_MODULE_2__.Validators.maxLength(Number(curr.value)),
              'Theia::Validation::Required': _angular_forms__WEBPACK_IMPORTED_MODULE_2__.Validators.required,
              'Theia::Validation::Pattern': _angular_forms__WEBPACK_IMPORTED_MODULE_2__.Validators.pattern(String(curr.value))
            };
            const validatorFn = validationTypeMap[curr.type];
            if (validatorFn) {
              prev.push(validatorFn);
            }
            return prev;
          }, []);
        }
      }
      return result || [];
    }
    initializeSelectControls(formGroup, selectControls, controls) {
      selectControls.forEach(control => {
        if (control.type === _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaControl.Select || control.type === _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaControl.MultiSelect) {
          const formControl = formGroup.get(control.id);
          const disableOption = option => {
            if (!option) {
              return;
            }
            const optionValue = option;
            let selectedOption;
            if (optionValue.type && optionValue.type === _models_template__WEBPACK_IMPORTED_MODULE_4__.TheiaType.DataOption) {
              selectedOption = optionValue;
            } else if (option) {
              // is string
              const selected = control.options?.find(opt => {
                if (typeof opt.value === 'string') {
                  return opt.value === option;
                }
                return opt.value.value === option;
              });
              if (selected) {
                selectedOption = selected.value;
              } else {
                return;
              }
            } else {
              return;
            }
            (selectedOption.disableControls || []).forEach(id => {
              const control = formGroup.get(id);
              if (control) {
                setTimeout(() => {
                  control.disable();
                }, 1);
              }
            });
            (selectedOption.enableControls || []).forEach(id => {
              const control = formGroup.get(id);
              if (control) {
                setTimeout(() => {
                  control.enable();
                }, 1);
              }
            });
            (selectedOption.hideControls || []).forEach(id => {
              const control = this.findControl(id, controls);
              if (control) {
                setTimeout(() => {
                  control.hidden = true;
                  formGroup.get(id)?.disable();
                }, 1);
              }
            });
            (selectedOption.showControls || []).forEach(id => {
              const control = this.findControl(id, controls);
              if (control) {
                setTimeout(() => {
                  control.hidden = false;
                  formGroup.get(id)?.enable();
                }, 1);
              }
            });
          };
          const selected = formControl?.value;
          if (selected) {
            const selectedOption = control.options?.find(option => {
              if (typeof option.value === 'string') {
                return option.value === selected;
              }
              return option.value.value === selected;
            });
            if (selectedOption) {
              disableOption(selectedOption.value);
            }
          }
          if (formControl) {
            formControl.valueChanges.subscribe(disableOption);
          }
        }
      });
    }
    initializeDependencyControls(formGroup, dependencyControls) {
      dependencyControls.forEach(control => {
        const dependencyControl = this.getDependencyControl(formGroup, control);
        const formControl = formGroup.get(control.id);
        if (dependencyControl && (control.type === _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaControl.Select || control.type === _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaControl.MultiSelect)) {
          dependencyControl.valueChanges.subscribe(value => {
            if (value.data) {
              const field = control?.dependency?.field;
              const datasourceDependency = control?.dependency?.datasourceDependency;
              if (field) {
                const newValue = value.data[control?.dependency?.field];
                if (datasourceDependency) {
                  const newDatasource = new URL(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/${control.datasource}`, this.window.location.origin);
                  newDatasource.searchParams.set(field, newValue);
                  control.datasource = newDatasource.pathname.replace(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/`, '') + newDatasource.search;
                } else {
                  formControl?.setValue(newValue);
                }
              }
            }
          });
        }
      });
    }
    getDependencyControl(formGroup, control) {
      return !(0,_models_template_control__WEBPACK_IMPORTED_MODULE_3__.isComplexControl)(control) && control.dependency?.controlId ? formGroup.get(control.dependency?.controlId) : undefined;
    }
    initializeDynamicDatasourceControls(formGroup, dynamicDatasourceControls, stepControls) {
      dynamicDatasourceControls.forEach(control => {
        if ((0,_models_template_control__WEBPACK_IMPORTED_MODULE_3__.hasDatasource)(control)) {
          const rx = /\${(.*?)}/g;
          let result;
          const updateDatasource = () => {
            control.datasource = '';
            //this.ref.tick();
            control.datasource = control.dynamic_datasource?.replace(rx, (_, id) => {
              const value = formGroup.get(id)?.value;
              const text = value && value.value ? value.value : value;
              return text || '';
            });
          };
          while (result = rx.exec(control.dynamic_datasource)) {
            const id = result[1];
            if (id) {
              const controlType = this.getControlType(id, stepControls);
              const formControl = formGroup.get(id);
              if ([_models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaControl.Select, _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaControl.MultiSelect, _models_template__WEBPACK_IMPORTED_MODULE_1__.TheiaControl.Toggle].includes(controlType)) {
                formControl?.valueChanges.subscribe(updateDatasource);
              } else {
                formControl?.valueChanges.pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_5__.distinctUntilChanged)(), (0,rxjs_operators__WEBPACK_IMPORTED_MODULE_6__.debounceTime)(1000), (0,rxjs_operators__WEBPACK_IMPORTED_MODULE_7__.filter)(v => v && v.length > 3)).subscribe(updateDatasource);
              }
            }
          }
          updateDatasource();
        }
      });
    }
    getControlType(id, controls) {
      return this.findControl(id, controls)?.type;
    }
    findControl(id, controls) {
      return controls?.find(control => control.id === id);
    }
    static #_ = this.ɵfac = function DynamicFormService_Factory(t) {
      return new (t || DynamicFormService)(_angular_core__WEBPACK_IMPORTED_MODULE_8__["ɵɵinject"](_angular_forms__WEBPACK_IMPORTED_MODULE_2__.UntypedFormBuilder), _angular_core__WEBPACK_IMPORTED_MODULE_8__["ɵɵinject"](_window_ref_service__WEBPACK_IMPORTED_MODULE_9__.WindowRefService), _angular_core__WEBPACK_IMPORTED_MODULE_8__["ɵɵinject"](_command_service__WEBPACK_IMPORTED_MODULE_10__.CommandService), _angular_core__WEBPACK_IMPORTED_MODULE_8__["ɵɵinject"](_data_source_service__WEBPACK_IMPORTED_MODULE_11__.DataSourceService));
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_8__["ɵɵdefineInjectable"]({
      token: DynamicFormService,
      factory: DynamicFormService.ɵfac,
      providedIn: 'root'
    });
  }
  return DynamicFormService;
})();

/***/ }),

/***/ 3807:
/*!**************************************************!*\
  !*** ./src/app/services/environment.resolver.ts ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   environmentResolver: () => (/* binding */ environmentResolver)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ 4980);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ 2389);
/* harmony import */ var _environment_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./environment.service */ 1574);




const environmentResolver = (route, state) => {
  const environmentService = (0,_angular_core__WEBPACK_IMPORTED_MODULE_0__.inject)(_environment_service__WEBPACK_IMPORTED_MODULE_1__.EnvironmentService);
  if (environmentService.environments$.value?.length) {
    return environmentService.environments$.value;
  }
  return environmentService.getEnvironments().pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_2__.catchError)(() => (0,rxjs__WEBPACK_IMPORTED_MODULE_3__.of)([])));
};

/***/ }),

/***/ 1574:
/*!*************************************************!*\
  !*** ./src/app/services/environment.service.ts ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   EnvironmentService: () => (/* binding */ EnvironmentService)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ 8071);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ 3738);
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../environments/environment */ 553);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ 4860);
/* harmony import */ var _local_storage_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./local-storage.service */ 3683);
/* harmony import */ var _allowed_apps_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./allowed-apps.service */ 9726);







let EnvironmentService = /*#__PURE__*/(() => {
  class EnvironmentService {
    constructor(http, localStorage, app) {
      this.http = http;
      this.localStorage = localStorage;
      this.app = app;
      this.currentEnvironment$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject(undefined);
      this.environments$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject(undefined);
      this.highlightedActions$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject([]);
      this.environmentsTree$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject([]);
      this.recentEnvironments$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject(undefined);
    }
    getEnvironments() {
      return this.http.get(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/data?type=profile`).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_2__.tap)(response => {
        this.environments$.next(response);
        this.environmentsTree$.next(this.generateEnvironmentsTree(response));
      }));
    }
    getSelectedEnvironment() {
      return this.getEnvironmentByName(this.loadEnvironmentMap()[this.app.selectedApp$.value]?.selected ?? "");
    }
    getCurrentEnvironment() {
      if (!this.currentEnvironment$.getValue()) {
        const env = this.getSelectedEnvironment();
        if (env) {
          this.currentEnvironment$.next(env);
        }
      }
      this.setHighlightedActions();
      return this.currentEnvironment$;
    }
    loadEnvironmentMap() {
      const envMap = this.localStorage.getItem('environmentData') ?? "{}";
      try {
        return JSON.parse(envMap);
      } catch (e) {
        return {};
      }
    }
    getRecentEnvironments() {
      if (!this.recentEnvironments$.getValue()) {
        const data = this.loadEnvironmentMap();
        const app = data[this.app.selectedApp$.value] || {};
        const recent = (app.recent || []).map(e => this.getEnvironmentByName(e));
        this.recentEnvironments$.next(recent);
      }
      return this.recentEnvironments$;
    }
    setCurrentEnvironment(env) {
      const data = this.loadEnvironmentMap();
      const recent = new Set(data[this.app.selectedApp$.value]?.recent || []);
      if (recent.has(env.name)) {
        recent.delete(env.name);
      }
      data[this.app.selectedApp$.value] = {
        selected: env.name,
        recent: [env.name, ...recent].slice(0, 6)
      };
      this.localStorage.setItem('environmentData', JSON.stringify(data));
      this.currentEnvironment$.next(env);
      this.recentEnvironments$.next(data[this.app.selectedApp$.value].recent.map(e => this.getEnvironmentByName(e)));
      this.setHighlightedActions();
    }
    getEnvironmentByName(name) {
      return this.environments$.value?.find(env => env.name === name);
    }
    setHighlightedActions() {
      const getActiveActions = (options, actions = []) => {
        if (options && options.length) {
          let result = [...actions];
          for (const option of options) {
            if (option.checked && option.actions) {
              result = [...result, ...option.actions, ...getActiveActions(option.children)];
            }
          }
          return result;
        } else {
          return actions;
        }
      };
      this.highlightedActions$.next(getActiveActions(this.currentEnvironment$.value?.wizard));
    }
    generateEnvironmentsTree(environments) {
      const tree = environments.reduce((prev, curr) => {
        if (!prev[curr.client]) {
          prev[curr.client] = {};
        }
        if (!prev[curr.client][curr.workload]) {
          prev[curr.client][curr.workload] = {};
        }
        prev[curr.client][curr.workload][curr.env] = curr;
        return prev;
      }, {});
      return Object.entries(tree).map(([key, value]) => ({
        name: key,
        children: Object.entries(value).map(([key, value]) => ({
          name: key,
          children: Object.entries(value).map(([key, value]) => ({
            name: key,
            env: value
          }))
        }))
      }));
    }
    static #_ = this.ɵfac = function EnvironmentService_Factory(t) {
      return new (t || EnvironmentService)(_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_4__.HttpClient), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵinject"](_local_storage_service__WEBPACK_IMPORTED_MODULE_5__.LocalStorageService), _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵinject"](_allowed_apps_service__WEBPACK_IMPORTED_MODULE_6__.AllowedAppsService));
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdefineInjectable"]({
      token: EnvironmentService,
      factory: EnvironmentService.ɵfac,
      providedIn: 'root'
    });
  }
  return EnvironmentService;
})();

/***/ }),

/***/ 957:
/*!******************************************!*\
  !*** ./src/app/services/info.service.ts ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   InfoService: () => (/* binding */ InfoService)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! rxjs */ 8071);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 1699);


let InfoService = /*#__PURE__*/(() => {
  class InfoService {
    set data(value) {
      this.data$.next(value);
    }
    get enabled() {
      return this.enabled$.value;
    }
    set enabled(value) {
      this.enabled$.next(value);
    }
    constructor() {
      this.data$ = new rxjs__WEBPACK_IMPORTED_MODULE_0__.BehaviorSubject('');
      this.enabled$ = new rxjs__WEBPACK_IMPORTED_MODULE_0__.BehaviorSubject(false);
    }
    showInfoPanel(data) {
      this.data = data;
      this.enabled = true;
    }
    disable() {
      this.enabled = false;
    }
    static #_ = this.ɵfac = function InfoService_Factory(t) {
      return new (t || InfoService)();
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineInjectable"]({
      token: InfoService,
      factory: InfoService.ɵfac,
      providedIn: 'root'
    });
  }
  return InfoService;
})();

/***/ }),

/***/ 3683:
/*!***************************************************!*\
  !*** ./src/app/services/local-storage.service.ts ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   LocalStorageService: () => (/* binding */ LocalStorageService)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _window_ref_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./window-ref.service */ 6889);


let LocalStorageService = /*#__PURE__*/(() => {
  class LocalStorageService {
    constructor(windowRef) {
      this.windowRef = windowRef;
      this.window = windowRef.nativeWindow;
    }
    getItem(key) {
      return this.window.localStorage.getItem(key);
    }
    setItem(key, value) {
      this.window.localStorage.setItem(key, value);
    }
    static #_ = this.ɵfac = function LocalStorageService_Factory(t) {
      return new (t || LocalStorageService)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"](_window_ref_service__WEBPACK_IMPORTED_MODULE_1__.WindowRefService));
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjectable"]({
      token: LocalStorageService,
      factory: LocalStorageService.ɵfac,
      providedIn: 'root'
    });
  }
  return LocalStorageService;
})();

/***/ }),

/***/ 2553:
/*!*****************************************!*\
  !*** ./src/app/services/log.service.ts ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   LogService: () => (/* binding */ LogService)
/* harmony export */ });
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs/operators */ 9736);
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../environments/environment */ 553);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common/http */ 4860);




let LogService = /*#__PURE__*/(() => {
  class LogService {
    constructor(http) {
      this.http = http;
    }
    getLog(name) {
      return this.http.get(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/log/${name}`).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_1__.map)(response => response.log));
    }
    static #_ = this.ɵfac = function LogService_Factory(t) {
      return new (t || LogService)(_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_3__.HttpClient));
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdefineInjectable"]({
      token: LogService,
      factory: LogService.ɵfac,
      providedIn: 'root'
    });
  }
  return LogService;
})();

/***/ }),

/***/ 6751:
/*!********************************************!*\
  !*** ./src/app/services/logout.service.ts ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   LogoutService: () => (/* binding */ LogoutService)
/* harmony export */ });
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../environments/environment */ 553);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ 4860);



let LogoutService = /*#__PURE__*/(() => {
  class LogoutService {
    constructor(http) {
      this.http = http;
    }
    logout() {
      return this.http.get(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/logout`);
    }
    static #_ = this.ɵfac = function LogoutService_Factory(t) {
      return new (t || LogoutService)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_2__.HttpClient));
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineInjectable"]({
      token: LogoutService,
      factory: LogoutService.ɵfac,
      providedIn: 'root'
    });
  }
  return LogoutService;
})();

/***/ }),

/***/ 8427:
/*!***********************************************!*\
  !*** ./src/app/services/s3-upload.service.ts ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   S3UploadService: () => (/* binding */ S3UploadService)
/* harmony export */ });
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../environments/environment */ 553);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ 4860);
/* harmony import */ var _environment_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./environment.service */ 1574);




let S3UploadService = /*#__PURE__*/(() => {
  class S3UploadService {
    constructor(http, environmentService) {
      this.http = http;
      this.environmentService = environmentService;
    }
    getSignedUrl(endpoint = '', fileType = '', fileName = '') {
      const env = this.environmentService.getCurrentEnvironment().value?.name;
      const params = `&env=${env}&file_name=${fileName}&file_type=${fileType}`;
      return this.http.get(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/${endpoint}${params}`);
    }
    static #_ = this.ɵfac = function S3UploadService_Factory(t) {
      return new (t || S3UploadService)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_2__.HttpClient), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵinject"](_environment_service__WEBPACK_IMPORTED_MODULE_3__.EnvironmentService));
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineInjectable"]({
      token: S3UploadService,
      factory: S3UploadService.ɵfac,
      providedIn: 'root'
    });
  }
  return S3UploadService;
})();

/***/ }),

/***/ 8554:
/*!*****************************************!*\
  !*** ./src/app/services/sse.service.ts ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SSEService: () => (/* binding */ SSEService)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! rxjs */ 2235);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 1699);


let SSEService = /*#__PURE__*/(() => {
  class SSEService {
    constructor() {}
    createEventSource(endpoint) {
      const eventSource = new EventSource(endpoint);
      return new rxjs__WEBPACK_IMPORTED_MODULE_0__.Observable(observer => {
        eventSource.onmessage = event => observer.next(event.data);
        eventSource.onerror = observer.error;
      });
    }
    static #_ = this.ɵfac = function SSEService_Factory(t) {
      return new (t || SSEService)();
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineInjectable"]({
      token: SSEService,
      factory: SSEService.ɵfac,
      providedIn: 'root'
    });
  }
  return SSEService;
})();

/***/ }),

/***/ 908:
/*!***********************************************!*\
  !*** ./src/app/services/template.resolver.ts ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   templateResolver: () => (/* binding */ templateResolver)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ 7947);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! rxjs */ 4980);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ 3738);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ 25);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs/operators */ 2389);
/* harmony import */ var _template_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./template.service */ 529);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ 6575);






const templateResolver = (route, state) => {
  const templateService = (0,_angular_core__WEBPACK_IMPORTED_MODULE_0__.inject)(_template_service__WEBPACK_IMPORTED_MODULE_1__.TemplateService);
  const document = (0,_angular_core__WEBPACK_IMPORTED_MODULE_0__.inject)(_angular_common__WEBPACK_IMPORTED_MODULE_2__.DOCUMENT);
  const router = (0,_angular_core__WEBPACK_IMPORTED_MODULE_0__.inject)(_angular_router__WEBPACK_IMPORTED_MODULE_3__.Router);
  if (templateService.template$.value) {
    return templateService.template$.value;
  }
  return templateService.getVerifyStatus().pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_4__.tap)(data => {
    validateStatus(data, state, document, router);
  }), (0,rxjs_operators__WEBPACK_IMPORTED_MODULE_5__.switchMapTo)(templateService.getTemplate()), (0,rxjs_operators__WEBPACK_IMPORTED_MODULE_6__.catchError)(() => (0,rxjs__WEBPACK_IMPORTED_MODULE_7__.of)(null)));
};
const validateStatus = (status, state, document, router) => {
  if (status?.redirect && state.url !== status.redirect) {
    if (isExternalURL(status.redirect)) {
      document.location.href = status.redirect;
    } else {
      router.navigateByUrl(status.redirect);
    }
  }
};
const isExternalURL = url => {
  return /^https?:\/{2}\S+$/.test(url);
};

/***/ }),

/***/ 529:
/*!**********************************************!*\
  !*** ./src/app/services/template.service.ts ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TemplateService: () => (/* binding */ TemplateService)
/* harmony export */ });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ 8071);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ 4980);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! rxjs */ 4300);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ 2607);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ 3738);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs/operators */ 9736);
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../environments/environment */ 553);
/* harmony import */ var _models_template__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../models/template */ 5339);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/common/http */ 4860);
/* harmony import */ var _environment_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./environment.service */ 1574);







let TemplateService = /*#__PURE__*/(() => {
  class TemplateService {
    constructor(http, environmentService) {
      this.http = http;
      this.environmentService = environmentService;
      this.template$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject(undefined);
      this.accountStatus$ = new rxjs__WEBPACK_IMPORTED_MODULE_1__.BehaviorSubject(undefined);
    }
    getTemplate() {
      return this.http.get(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/template`).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_2__.mergeMap)(data => this.loadObjectRefs(data)), (0,rxjs_operators__WEBPACK_IMPORTED_MODULE_3__.tap)(data => this.template$.next(data)));
    }
    getVerifyStatus() {
      return this.http.get(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/verify_status`).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_3__.tap)(data => this.accountStatus$.next(data)));
    }
    getDiagramData(endpoint, defaultValue) {
      if (!endpoint) {
        return (0,rxjs__WEBPACK_IMPORTED_MODULE_4__.of)(defaultValue);
      }
      const env = this.environmentService.getCurrentEnvironment().value;
      if (!env) {
        return (0,rxjs__WEBPACK_IMPORTED_MODULE_4__.of)(defaultValue);
      }
      return this.http.get(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/${endpoint}?env=${env.name}`);
    }
    getSectionByRoute(route) {
      const template = this.template$.getValue();
      return template?.sections.find(section => section.type === _models_template__WEBPACK_IMPORTED_MODULE_5__.TheiaType.Section && section.route === route);
    }
    getFirstRoute() {
      const template = this.template$.getValue();
      const first = template?.sections[0];
      return first?.type === _models_template__WEBPACK_IMPORTED_MODULE_5__.TheiaType.Section ? first.route : '';
    }
    getActionById(route, id) {
      const section = this.getSectionByRoute(route);
      return section?.actions?.find(action => action.id === id);
    }
    loadObjectRefs(data) {
      const observables = {};
      for (const key of Object.keys(data)) {
        if (key === '$ref' && data[key]) {
          observables[key] = this.http.get(`${_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.apiUrl}/${data.$ref}`).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_2__.mergeMap)(data => this.loadObjectRefs(data)));
        } else if (Array.isArray(data[key]) && data[key].length) {
          observables[key] = this.loadObjectRefs(data[key]).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_6__.map)(res => Object.entries(res).reduce((acc, [key, value]) => {
            acc[key] = value;
            return acc;
          }, [])));
        } else if (!Array.isArray(data[key]) && typeof data[key] === 'object' && data[key] !== null) {
          observables[key] = this.loadObjectRefs(data[key]);
        } else {
          observables[key] = (0,rxjs__WEBPACK_IMPORTED_MODULE_4__.of)(data[key]);
        }
      }
      return (0,rxjs__WEBPACK_IMPORTED_MODULE_7__.forkJoin)(observables).pipe((0,rxjs_operators__WEBPACK_IMPORTED_MODULE_2__.mergeMap)(res => {
        const result = {
          ...data,
          ...res,
          ...res['$ref']
        };
        delete result['$ref'];
        return (0,rxjs__WEBPACK_IMPORTED_MODULE_4__.of)(result);
      }));
    }
    loadDynamicTemplate(url) {
      return this.http.get(url);
    }
    static #_ = this.ɵfac = function TemplateService_Factory(t) {
      return new (t || TemplateService)(_angular_core__WEBPACK_IMPORTED_MODULE_8__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_9__.HttpClient), _angular_core__WEBPACK_IMPORTED_MODULE_8__["ɵɵinject"](_environment_service__WEBPACK_IMPORTED_MODULE_10__.EnvironmentService));
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_8__["ɵɵdefineInjectable"]({
      token: TemplateService,
      factory: TemplateService.ɵfac,
      providedIn: 'root'
    });
  }
  return TemplateService;
})();

/***/ }),

/***/ 6889:
/*!************************************************!*\
  !*** ./src/app/services/window-ref.service.ts ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   WindowRefService: () => (/* binding */ WindowRefService)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);

function getWindow() {
  return window;
}
let WindowRefService = /*#__PURE__*/(() => {
  class WindowRefService {
    get nativeWindow() {
      return getWindow();
    }
    static #_ = this.ɵfac = function WindowRefService_Factory(t) {
      return new (t || WindowRefService)();
    };
    static #_2 = this.ɵprov = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjectable"]({
      token: WindowRefService,
      factory: WindowRefService.ɵfac,
      providedIn: 'root'
    });
  }
  return WindowRefService;
})();

/***/ }),

/***/ 553:
/*!*****************************************!*\
  !*** ./src/environments/environment.ts ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   environment: () => (/* binding */ environment)
/* harmony export */ });
// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.
const environment = {
  production: false,
  apiUrl: '/api',
  auth0: {
    domain: 'rapidcloud-dev.us.auth0.com',
    clientId: '1Tkeu4gJ3n9o5knNyDT6QtnVTD6XU7UA'
  },
  authorizationParams: {
    audience: 'https://rapid-cloud.io'
  },
  baseHref: '/app/',
  redirectUri: '/app'
};
/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.

/***/ }),

/***/ 4913:
/*!*********************!*\
  !*** ./src/main.ts ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/platform-browser */ 6480);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _app_app_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./app/app.module */ 8629);
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./environments/environment */ 553);




if (_environments_environment__WEBPACK_IMPORTED_MODULE_0__.environment.production) {
  (0,_angular_core__WEBPACK_IMPORTED_MODULE_1__.enableProdMode)();
}
_angular_platform_browser__WEBPACK_IMPORTED_MODULE_2__.platformBrowser().bootstrapModule(_app_app_module__WEBPACK_IMPORTED_MODULE_3__.AppModule).catch(err => console.error(err));

/***/ }),

/***/ 3653:
/*!*******************************************************************************!*\
  !*** ./src/app/components/ lazy ^\.\/.*\/.*\.component\.ts$ namespace object ***!
  \*******************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var map = {
	"./accordion/components/accordion-item/accordion-item.component.ts": 2836,
	"./accordion/components/accordion/accordion.component.ts": 1638,
	"./actions/actions.component.ts": 3494,
	"./architecture-wizard/architecture-wizard.component.ts": 7204,
	"./architecture/architecture.component.ts": 7433,
	"./auth-error/auth-error.component.ts": 6410,
	"./composite-group/composite-group.component.ts": 2096,
	"./confirm-modal/confirm-modal.component.ts": 6530,
	"./dashboard/components/dashboard/dashboard.component.ts": 5863,
	"./dashboard/components/panel-markdown/panel-markdown.component.ts": 169,
	"./dashboard/components/panel-table/panel-table.component.ts": 522,
	"./diagram/diagram.component.ts": 7254,
	"./dynamic-action/dynamic-action.component.ts": 334,
	"./dynamic-control/dynamic-control.component.ts": 1081,
	"./dynamic-form/dynamic-form.component.ts": 3439,
	"./dynamic-section/dynamic-section.component.ts": 1954,
	"./error/error.component.ts": 9426,
	"./footer/footer.component.ts": 7913,
	"./grid/grid.component.ts": 3150,
	"./header/header.component.ts": 6471,
	"./home/home.component.ts": 159,
	"./info/info.component.ts": 3636,
	"./key-value-editor/key-value-editor.component.ts": 1052,
	"./layout/layout.component.ts": 2952,
	"./modal/modal.component.ts": 354,
	"./not-found/not-found.component.ts": 6218,
	"./pagination/pagination.component.ts": 2649,
	"./readme/readme.component.ts": 7350,
	"./sidebar/sidebar.component.ts": 7954,
	"./steps/steps.component.ts": 5770,
	"./tab-bar/tab-bar.component.ts": 7354,
	"./type-ahead/type-ahead.component.ts": 3858
};

function webpackAsyncContext(req) {
	return Promise.resolve().then(() => {
		if(!__webpack_require__.o(map, req)) {
			var e = new Error("Cannot find module '" + req + "'");
			e.code = 'MODULE_NOT_FOUND';
			throw e;
		}

		var id = map[req];
		return __webpack_require__(id);
	});
}
webpackAsyncContext.keys = () => (Object.keys(map));
webpackAsyncContext.id = 3653;
module.exports = webpackAsyncContext;

/***/ })

},
/******/ __webpack_require__ => { // webpackRuntimeModules
/******/ var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
/******/ __webpack_require__.O(0, ["vendor"], () => (__webpack_exec__(4913)));
/******/ var __webpack_exports__ = __webpack_require__.O();
/******/ }
]);
//# sourceMappingURL=main.js.map