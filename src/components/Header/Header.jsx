import React from "react";
// import Header component from the semantic-ui-react
import { Header } from "semantic-ui-react";
import "./header.css";


function AppDashboard() {
  return (
    <div>
      <Header as="h2" block>
      <img
  src={process.env.PUBLIC_URL + '/logo.png'}
  alt="Logo"
  style={{ width: '120px', height: '70px' }}
/>
      </Header>
    </div>
  );
}

export default AppDashboard;
