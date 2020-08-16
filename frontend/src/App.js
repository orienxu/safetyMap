import React, { Component } from 'react';
import './App.css';
import GoogleMapReact from 'google-map-react';
import Title from './res/crimepredicttitle.png';
import redDot from './res/red-dot.png';
import greenDot from './res/green-dot.png';
import yellowDot from './res/yellow-dot.png';
import SliderMin from './sliderMin';
import SliderHour from './sliderHour';
import SliderSec from './sliderSec';
import Marker from './marker/marker';

const AnyReactComponent = ({ text }) => <div>{text}</div>;

const getMapOptions = (maps) => {
  return {
    disableDefaultUI: true,
    mapTypeControl: true,
    streetViewControl: true,
    styles: [{ featureType: 'poi', elementType: 'labels', stylers: [{ visibility: 'on' }] }],
  };
};

export default class App extends Component {
  static defaultProps = {
    center: {
      lat: 47.58,
      lng: -122.3097
    },
    zoom: 12
  };

  constructor() {
    super();
    this.state = {
      crimes: {},
      mountTime: (new Date).getTime(),
    }
  }

  componentDidMount() {
    fetch("/crime").then(response =>
      response.json().then(data => {
        this.setState({ crimes: data });
      })
    );
  }

  handleClick() {
    const currentTime = (new Date).getTime();

    if (currentTime >= (this.state.mountTime + 4000)) {
      this.setState({ mountTime: currentTime })
      fetch("/crime").then(response =>
        response.json().then(data => {
          this.setState({ crimes: data });
        })
      );
    } else {
    }
  }

  renderMap() {
    return (
      // Important! Always set the container height explicitly
      <div style={{ height: '70vh', width: '100%' }}>
        <GoogleMapReact
          bootstrapURLKeys={{ key: 'AIzaSyCsHAjWr3yYjd6QNG0UHLI9u_J2WIRrVfE' }}
          defaultCenter={this.props.center}
          defaultZoom={this.props.zoom}
          options={getMapOptions}
        >
          {
            console.log('this.state.crime', this.state.crimes.list),
            this.state.crimes.list && this.state.crimes.list.map(({ lat, long }) => (
              // <img
              //   src={redDot}
              //   lat={lat * 10 + 0.0005}
              //   lng={long * 100 + 0.025}
              // />
              <Marker
                lat={lat}
                lng={long}
                name="My Marker"
                color="red"
              />
            ))
          }
        </GoogleMapReact>
      </div>
    );
  }

  renderInfo() {
    return (
      <div className="info" style={styles.info}>
        <div>
          <p>Select Day</p>
          <SliderHour color="#FF4136" />
        </div>
        <div>
          <p>Select Hour</p>
          <SliderMin color="#FF4136" />
        </div>
        <div>
          <p>Select Minute</p>
          <SliderSec color="#FF4136" />
        </div>
        <button onClick={() => this.handleClick()}>
          Search For Danger
        </button>
      </div>
    );
  }

  render() {
    return (
      <div className="container">
        <div className='header'>
          {/* <p style={styles.p1}>Welcome to Our Crime Prediction Site! </p>
          <p style={{ fontSize: 30, color: 'white' }}>Your Safety is Our Greatest Concern</p> */}
          <img src={Title} style={{ marginLeft: 35 }} />
        </div>
        <div className="body" style={styles.body}>
          <div className="map" style={styles.map}>
            {this.renderMap()}
          </div>
          {this.renderInfo()}
        </div>
      </div>
    );
  }
}

const styles = {
  p1: {
    fontSize: 30,
    color: 'white'
  },
  body: {
    width: '100%'
  },
  map: {
    width: '60%'
  },
  info: {
    width: '22%',
    backgroundColor: '#CEEED5',
  },
}