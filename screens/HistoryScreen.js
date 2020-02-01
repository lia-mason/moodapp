import React from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';
import { ExpoLinksView } from '@expo/samples';

export default function HistoryScreen() {
  return (
    <ScrollView style={styles.container}>
{/*           <View style={styles.getStartedContainer}>

          <Text style={styles.getStartedText}>Hello Lia!</Text>

          </View> */}
    </ScrollView>
  );
}

HistoryScreen.navigationOptions = {
  title: 'History',
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 20,
    backgroundColor: '#fff',
  },
  getStartedContainer: {
    alignItems: 'center',
    marginHorizontal: 0,
    flex : 1/6,
    backgroundColor: '#00CC99',
    height : 100,
    justifyContent: 'center',
    paddingTop: 20,
  },
  getStartedText: {
    fontSize: 30,
    color: 'white',
    lineHeight: 28,
    textAlign: 'center',
  },
});
