
//all client side stuff over here
if (Meteor.isClient) {
  var MAP_ZOOM = 10;
  var locations = [];


//function to get data from parse database and pass locations into an array
  function getData() {
    Parse.initialize("N2JqJz0aiZJCI8AsS54lIGS2ZPkIrnuAjjNwMDMp", "lifNBQyqt8tuG0GnSeOswmdHug1D1BV1FZyikMB2");

    var Location = Parse.Object.extend("location");
    var query = new Parse.Query(Location);

     query.find({
       success: function(results) { 
         console.log("Successfully retrieved " + results.length +  " scores.");

         var currentLocationCount = results.length;

         Session.set("locationCount", currentLocationCount);

         console.log(JSON.stringify(results));

         for (var i = 0; i < results.length; i++) {
           var magnitudes = results[i].get("Magnitude");
           console.log(magnitudes);

           var geoPoints = results[i].get("location");
           // console.log(JSON.stringify(geoPoints));

           var latitudeParse = geoPoints["latitude"];
           var longitudeParse = geoPoints["longitude"];

           // console.log(latitudeParse);
           // console.log(longitudeParse);
           locations[i] = new Array(3);

           locations[i][0] = latitudeParse;
           locations[i][1] = longitudeParse;
           locations[i][2] = magnitudes;

           console.log("Latitude No. " + i + " : " + locations[i][0]);
           console.log("longitude No. " + i + " : " + locations[i][1]);
           console.log("longitude No. " + i + " : " + locations[i][2]);


         }

         //the array that will be watched for changes
        Session.set("locations", locations);
       },

       error: function(object, error) {
         console.log("Error retrieving data from database");
       }
     });
  }

  Meteor.startup(function() {
    GoogleMaps.load();
  });

//when
  Template.map.onCreated(function() {
    var self = this;

    //get data from database every second
    Meteor.setInterval(getData, 1000);

    GoogleMaps.ready('map', function(map) {
      var marker = [];

      //create and update markers when number of locations in the database changes
      self.autorun(function() {

        //variable that is watched for changes
        Session.get("locations");

        console.log("The data has changed!");
        console.log("There are " + locations.length + " locations in the database");
          // for (i=0; i < locations.length; i++) {
          //
          // infowindow = new google.maps.InfoWindow({
          //     content:  "yo"
          // });
          //
          //   marker = new google.maps.Marker({
          //     position: new google.maps.LatLng(locations[i][0], locations[i][1]),
          //     animation: google.maps.Animation.DROP,
          //     map: map.instance
          //   });
          //   google.maps.event.addListener(marker, 'click', function(marker, i) {
          //     infowindow.open(map.instance, marker);
          //   })(marker, i);
          // }

          for (i = 0; i < locations.length; i++) {

            var pinIcon = new google.maps.MarkerImage(
                "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|FFFF00",
                null, /* size is determined at runtime */
                null, /* origin is 0,0 */
                null, /* anchor is bottom center of the scaled image */
                new google.maps.Size(10, 10)
            );

            marker = new google.maps.Marker({
              position: new google.maps.LatLng(locations[i][0], locations[i][1]),
              animation: google.maps.Animation.DROP,
              map: map.instance
            });

            marker.info = new google.maps.InfoWindow({
                content:  "Magnitude: " + "<b>" + locations[i][2] + "</b>"
            });

            google.maps.event.addListener(marker, 'click', (function(marker, i) {
              return function() {
                marker.info.open(map.instance, marker);
              }
            })(marker, i));
          }


          console.log("There are: " + marker.length + " markers");
      });

      // Center and zoom the map view onto the current position.
      // map.instance.setCenter(marker.getPosition());
      map.instance.setZoom(MAP_ZOOM);
    });
  });

  Template.map.helpers({
    geolocationError: function() {
      var error = Geolocation.error();
      return error && error.message;
    },
    mapOptions: function() {
      var latLng = Geolocation.latLng();
      // Initialize the map once we have the latLng.
      if (GoogleMaps.loaded() && latLng) {
        return {
          center: new google.maps.LatLng(latLng.lat, latLng.lng),
          zoom: MAP_ZOOM
        };
      }
    },
    locationCount: function() {
      var locationCount = Session.get("locationCount");
      return locationCount;
    }
  });

  Template.sidebar.events({
    "click .sidebar-button": function (event) {
      console.log("hi");
      $('.md-modal').fadeIn( "slow", function() {
        // Animation complete
      });
    },
    "click .md-close": function (event) {
      console.log("bye");
      $('.md-modal').fadeOut( "slow", function() {
        // Animation complete
      });
    }

  });
}


//all server side stuff here
if (Meteor.isServer) {
  Meteor.startup(function () {
    // code to run on server at startup

  });
}
