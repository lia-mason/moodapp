import * as WebBrowser from 'expo-web-browser';
import React from 'react';
import {
  Image,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { TextInput} from 'react-native-paper';
import Smile from './smile.png';

import { MonoText } from '../components/StyledText';

export default class HomeScreen extends React.Component {

  state = {
    text: ''
  };

  render(){
    return (
      <View style={styles.container}>
        <ScrollView
          style={styles.container}
          contentContainerStyle={styles.contentContainer}>
          <View style={styles.welcomeContainer}>
          </View>

          <View style={styles.getStartedContainer}>

            <Text style={styles.getStartedText}>Hello Lia!</Text>

          </View>

          <View style={styles.questionContainer}>

            <Text style={styles.questionText}>How are you feeling?</Text>

          </View>

          <View style={{flex:1}}>
         
          <View style={styles.textboxContainer}>

            <TextInput
                  style={{paddingVertical:50}, {paddingHorizontal:20}}
                  selectionColor='#00CC99'
                  underlineColor='#00CC99'
                  theme={{ colors: { primary: '#006666',underlineColor:'transparent',}}}
                  mode='outlined'
                  placeholder=''
                  value={this.state.text}
                  onChangeText={text => this.setState({ text })}
                  multiline='true'
              />
          
          </View>

          <View style={styles.imageContainer}>

            <Image source={require('./smile.png')} style={{width: 200, height: 200}}/>

          </View>

          </View>

        </ScrollView>
        </View>
    );
  }
}

HomeScreen.navigationOptions = {
  header: null,
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  developmentModeText: {
    marginBottom: 20,
    color: '#00CC99',
    fontSize: 14,
    lineHeight: 19,
    textAlign: 'center',
  },
  contentContainer: {
    paddingTop: 0,
  },
  questionContainer: {
    flex:1,
    paddingTop: 40,
  },
  textboxContainer: {
    flex:1,
    paddingTop: 40,
  },
  welcomeContainer: {
    alignItems: 'center',
    marginTop: 0,
    marginBottom: 0,
  },
  imageContainer: {
    alignItems: 'center',
    marginTop: 70,
    marginBottom: 0,
  },
  welcomeImage: {
    width: 100,
    height: 80,
    resizeMode: 'contain',
    marginTop: 0,
    marginLeft: 0,
    alignItems: 'center',
    justifyContent: 'center',
    paddingLeft: 50
  },
  getStartedContainer: {
    alignItems: 'center',
    marginHorizontal: 0,
    flex : 1/6,
    backgroundColor: '#00CC99',
    height : 100,
    justifyContent: 'center',
    paddingTop: 20,
    shadowOffset:{  width: 0,  height: 5,  },
    shadowColor: 'black',
    shadowOpacity: 0.2,
  },
  homeScreenFilename: {
    marginVertical: 7,
  },
  codeHighlightText: {
    color: '#00CC99',
  },
  codeHighlightContainer: {
    backgroundColor: '#00CC99',
    borderRadius: 3,
    paddingHorizontal: 4,
  },
  getStartedText: {
    fontSize: 30,
    color: 'white',
    lineHeight: 28,
    textAlign: 'center',
  },
  questionText: {
    fontSize: 30,
    color: 'black',
    lineHeight: 0,
    textAlign: 'center',
    paddingHorizontal: 0
  },
  tabBarInfoContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    ...Platform.select({
      ios: {
        shadowColor: 'black',
        shadowOffset: { width: 0, height: -3 },
        shadowOpacity: 0.1,
        shadowRadius: 3,
      },
      android: {
        elevation: 20,
      },
    }),
    alignItems: 'center',
    backgroundColor: '#fbfbfb',
    paddingVertical: 20,
  },
  tabBarInfoText: {
    fontSize: 17,
    color: '#00CC99',
    textAlign: 'center',
  },
  navigationFilename: {
    marginTop: 5,
  },
  helpContainer: {
    marginTop: 15,
    alignItems: 'center',
  },
  helpLink: {
    paddingVertical: 15,
  },
  helpLinkText: {
    fontSize: 14,
    color: '#00CC99',
  },
});
