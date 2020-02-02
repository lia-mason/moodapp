import React from 'react';
import { Platform } from 'react-native';
import { createStackNavigator } from 'react-navigation-stack';
import { createBottomTabNavigator } from 'react-navigation-tabs';

import TabBarIcon from '../components/TabBarIcon';
import { Ionicons } from '@expo/vector-icons';
import HomeScreen from '../screens/HomeScreen';
import HistoryScreen from '../screens/HistoryScreen';
import SettingsScreen from '../screens/SettingsScreen';

const config = Platform.select({
  web: { headerMode: 'screen' },
  default: {},
});

const HomeStack = createStackNavigator(
  {
    Home: HomeScreen,
  },
  config
);

HomeStack.navigationOptions = {
  tabBarLabel: 'Home',
  tabBarOptions: { 
    activeTintColor: '#696969',
    inactiveTintColor: '#696969',
    style:{height:60}
  },
  tabBarIcon: ({ focused }) => (
    <TabBarIcon
    focused={focused} name={Platform.OS === 'ios' ? 'ios-home' : 'ios-home'} />
  ),
};

HomeStack.path = '';

const LinksStack = createStackNavigator(
  {
    Links: HistoryScreen,
  },
  config
);

LinksStack.navigationOptions = {
  tabBarLabel: 'History',
  tabBarOptions: { 
    activeTintColor: '#696969',
    inactiveTintColor: '#696969',
    style:{height:60}, 
  },
  tabBarIcon: ({ focused }) => (
    <TabBarIcon focused={focused} name={Platform.OS === 'ios' ? 'ios-clock' : 'ios-clock'} />
  ),
};

LinksStack.path = '';

const tabNavigator = createBottomTabNavigator({
  HomeStack,
  LinksStack,
});

tabNavigator.path = '';

export default tabNavigator;
