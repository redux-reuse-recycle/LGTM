import React from "react";
import { Route, Switch, Redirect } from "react-router-dom";
import FileList from "./containers/HomeContainer";
import FileViewer from './containers/FileViewerContainer';

const Routes = () => (
  <Switch>
    <Route path="/" exact component={FileList} />
    <Route path={"/file/:fileName"} component={FileViewer} />
    <Redirect to="/" />
  </Switch>
);

export default Routes;
