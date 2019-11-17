import React from "react";
import { Route, Switch, Redirect } from "react-router-dom";
import Home from "./containers/HomeContainer";

const Routes = () => (
  <Switch>
    <Route path="/" exact component={Home} />
    <Redirect to="/" />
  </Switch>
);

export default Routes;
