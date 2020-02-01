import React from 'react'
import {createStackNavigator} from "react-navigation-stack";
import Username from "./username";

const Stack = createStackNavigator();

class HomeScreen extends React.Component {
    static navigationOptions = {
      title: 'Welcome',
    };
    render() {
      const {navigate} = this.props.navigation;
      return (
        <Button
          title="Go to Jane's profile"
          onPress={() => navigate('Profile', {name: 'Jane'})}
        />
      );
    }
  }
