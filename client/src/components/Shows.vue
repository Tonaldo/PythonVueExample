<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>📺TV SHOWS📺</h1>
        <hr><br><br>
        <alert :message=message :showMessage.sync=showMessage v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.show-modal>Add TV show</button>

        <button type="button" class="btn btn-info btn-sm" @click="changeView()">List/poster mode</button>
        <button  type="button" class="btn btn-primary float-right btn-sm " @click="toggleWatchlist()">{{ !this.watchList ? 'Show watchlist' : 'Show all my shows' }}</button>
        <br><br>
        <table  v-if="listMode " class="table table-hover">
          <thead>
            <tr>
              <th @click="sortBy('title')" :style="{ 'cursor': 'pointer' }" scope="col">Title <span v-if="sortOrder === 'asc' && sortKey === 'title'"> <font-awesome-icon  icon="chevron-down" /></span> <span v-if="sortOrder === 'desc' && sortKey === 'title'"> <font-awesome-icon  icon="chevron-up" /></span> </th>
              <th @click="sortBy('year')"   :style="{ 'cursor': 'pointer' }"  scope="col">Year <span v-if="sortOrder === 'asc' && sortKey === 'year'"> <font-awesome-icon  icon="chevron-down" /></span> <span v-if="sortOrder === 'desc' && sortKey === 'year'"> <font-awesome-icon  icon="chevron-up" /></span> </th></th>
              <th @click="sortBy('watched')"  :style="{ 'cursor': 'pointer' }"  scope="col">Watched? <span v-if="sortOrder === 'asc' && sortKey === 'watched'"> <font-awesome-icon  icon="chevron-down" /></span> <span v-if="sortOrder === 'desc' && sortKey === 'watched'"> <font-awesome-icon  icon="chevron-up" /></span> </th></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr  v-for="(show, index) in showsSorted" :key="index">
              <td>{{ show.title }}</td>
              <td>{{ show.year }}</td>
              <td>
                <span v-if="show.watched">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <button
                        type="button"
                        class="btn btn-warning btn-sm"
                        v-b-modal.show-update-modal
                        @click="editShow(show)">
                    Update
                </button>
                <button
                        type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeleteShow(show)">
                    Delete
                </button>

                   <button v-if="!show.watchlist"
                        type="button"
                        class="btn btn-outline-primary btn-sm watchListTableBtn"
                        @click="onAddWatchlistShow(show)">
                    Watchlist
                </button>
                     <button v-if="show.watchlist"
                        type="button"
                        class="btn btn-outline-primary btn-sm watchListTableBtn"
                        @click="onWatchlistDelete(show)">
                    Remove from watchlist
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <carousel v-if="!listMode && !watchlist"  :scrollPerPage=true :perPage=1 :centerMode=true  :style="{'text-align': 'center'}">
  <slide v-for="(show, index) in showsSorted ">

     <img  @error="replace404"  :src="show.posterImg" :key="index"/>

  </slide>
</carousel>

      </div>
    </div>
    <b-modal ref="addShowModal"
             id="show-modal"
             title="Add a new show"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addShowForm.title"
                        required
                        trim
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-year-group"
                      label="Year:"
                      label-for="form-year-input">
            <b-form-input id="form-year-input"
                          type="number"
                          min="1920"
                          max="2019"
                          v-model="addShowForm.year"
                          required
                          placeholder="Enter year">
            </b-form-input>
          </b-form-group>

                <b-form-group id="form-year-edit-group"
                      label="Poster image url:"
                      label-for="form-year-edit-input">
            <b-form-input id="form-posterImg-edit-input"
                          type="text"
                          v-model="addShowForm.posterImg"
                          required
                          placeholder="Enter poster image URL">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-watched-group">
          <b-form-checkbox-group v-model="addShowForm.watched" id="form-checks">
            <b-form-checkbox value="true">Watched?</b-form-checkbox>
          </b-form-checkbox-group>
              <b-form-checkbox-group v-model="addShowForm.watchlist" id="form-checks">
               <b-form-checkbox value="true">Add to watchlist?</b-form-checkbox>
             </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" :disabled="errors.any()" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editShowModal"
             id="show-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-title-edit-group"
                    label="Title:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-year-edit-group"
                      label="Year:"
                      label-for="form-year-edit-input">
            <b-form-input id="form-year-edit-input"
                          type="text"
                          name="year"
                          v-model="editForm.year"
                          required
                          placeholder="Enter year">
            </b-form-input>
          </b-form-group>
               <b-form-group id="form-year-edit-group"
                      label="Poster image url:"
                      label-for="form-year-edit-input">
            <b-form-input id="form-year-edit-input"
                          type="text"
                          v-model="editForm.posterImg"
                          required
                          placeholder="Enter poster image URL">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-watched-edit-group">
          <b-form-checkbox-group v-model="editForm.watched" id="form-checks">
            <b-form-checkbox value="true">Watched?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';
import VeeValidate from 'vee-validate'
import { Carousel, Slide } from 'vue-carousel';
import _ from 'lodash';

export default {
  data() {
    return {
      shows: [],
      allShows: [],
      watchListShows: [],
      listMode: true,
      watchList: false,
      sortKey: 'title',
      sortOrder: 'asc',
      filter: '',
      addShowForm: {
        title: '',
        year: '',
        posterImg: '',
        watched: [],
        watchlist: []
      },
      editForm: {
        id: '',
        title: '',
        year: '',
        posterImg: '',
        watched: [],
        watchlist: []
      },
      message: '',
      showMessage: false,
       errorImg: require("../assets/404img.png")
            
    };
  },
  components: {
    alert: Alert,
    Carousel,
    Slide
  },
  
  computed: {
 
     showsSorted: function() {
         if(this.watchList === true) {
          this.watchListShows = this.shows.filter((show) => show.watchlist === true)
          return _.orderBy(this.watchListShows, this.sortKey, this.sortOrder);
        }
        else {
          return _.orderBy(this.allShows, this.sortKey, this.sortOrder);
        
        }
    }
},

  methods: {

    isNumber: function(n) {
      return !isNaN(parseFloat(n)) && isFinite(n);
    },

    replace404(e) {
      e.target.src = this.errorImg
    },

    sortBy: function(key) {
      if (key == this.sortKey) {
        this.sortOrder = (this.sortOrder == 'asc') ? 'desc' : 'asc';
      } else {
        this.sortKey = key;
        this.sortOrder = 'asc';
      }
     },

     validateState(ref) {
      console.log(this.veeFields[ref])
      console.log("yaas!")
        if (this.veeFields[ref] && (this.veeFields[ref].dirty || this.veeFields[ref].validated)) {
          return !this.errors.has(ref)
        }
        return null
      },

    changeView: function() {
      this.listMode = !this.listMode
    },
    toggleWatchlist: function() {
      this.watchList = !this.watchList
    },

    getShows() {
      const path = 'https://pythonvueapi.herokuapp.com/shows';
      axios.get(path)
        .then((res) => {
          this.shows = this.allShows = res.data.shows;  
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addShow(payload) {
      payload.id = Math.random().toString(36).substr(2, 5);
      const path = 'https://pythonvueapi.herokuapp.com/shows';
      axios.post(path, payload)
        .then(() => {
          this.getShows();
          this.message = 'Show added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getShows();
        });
    },
    updateShow(payload, showID) {
      const path = `https://pythonvueapi.herokuapp.com/shows/${showID}`;
      axios.put(path, payload)
        .then(() => {
          this.getShows();
          this.message = 'Show updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getShows();
        });
    },
    removeShow(showID) {
      const path = `https://pythonvueapi.herokuapp.com/shows/${showID}`;
      axios.delete(path)
        .then(() => {
          this.getShows();
          this.message = 'Show removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getShows();
        });
    },

    AddWatchlistShow(showID) {
      const path = `https://pythonvueapi.herokuapp.com/shows/${showID}`;
      let payload = {};
      payload.watchlist = true;
      axios.put(path, payload)
        .then(() => {
          this.getShows();
          this.message = 'Show added to watchlist!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getShows();
        }); 
    },

    RemoveWatchlistShow(showID) {
     const path = `https://pythonvueapi.herokuapp.com/shows/${showID}`;
     let payload = {};
     payload.watchlist = false;
     axios.put(path, payload)
      .then(() => {
        this.getShows();
        this.message = 'Show removed from watchlist!';
        this.showMessage = true;
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.getShows();
      }); 
    },

    initForm() {
      this.addShowForm.title = '';
      this.addShowForm.year = '';
      this.addShowForm.posterImg = '';
      this.addShowForm.watched = [];
      this.addShowForm.watchlist = [];
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.year = '';
      this.editForm.posterImg = '';
      this.editForm.watched = [];
      this.editForm.watchlist = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addShowModal.hide();
      let watched = false;
      let watchlist = false;
      if (this.addShowForm.watched[0]) watched = true;
      if (this.addShowForm.watchlist[0]) watchlist = true;
      const payload = {
        title: this.addShowForm.title,
        year: this.addShowForm.year,
        posterImg: this.addShowForm.posterImg,
        watched,
        watchlist, // property shorthand
      };
      this.addShow(payload);
      this.initForm();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editShowModal.hide();
      let watched = false;
      if (this.editForm.watched[0]) watched = true;
      const payload = {
        title: this.editForm.title,
        year: this.editForm.year,
        watched,
      };
      this.updateShow(payload, this.editForm.id);
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addShowModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editShowModal.hide();
      this.initForm();
      this.getShows(); // why?
    },
    onDeleteShow(show) {
      this.removeShow(show.id);
    },
    onWatchlistDelete(show) {
      this.RemoveWatchlistShow(show.id);
    },
    onAddWatchlistShow(show) {
      this.AddWatchlistShow(show.id);
    },
    editShow(show) {
      this.editForm = show;
    },
  },

  created() {
    this.getShows();
  },
};
</script>
