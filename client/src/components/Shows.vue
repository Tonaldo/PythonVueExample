<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>📺TV SHOWS📺</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.show-modal>Add TV show</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th @click="sortBy('title')" :style="{ 'cursor': 'pointer' }" scope="col">Title <span v-if="sortOrder === 'asc' && sortKey === 'title'"> <font-awesome-icon  icon="chevron-down" /></span> <span v-if="sortOrder === 'desc' && sortKey === 'title'"> <font-awesome-icon  icon="chevron-up" /></span> </th>
              <th @click="sortBy('year')"   :style="{ 'cursor': 'pointer' }"  scope="col">Year <span v-if="sortOrder === 'asc' && sortKey === 'year'"> <font-awesome-icon  icon="chevron-down" /></span> <span v-if="sortOrder === 'desc' && sortKey === 'year'"> <font-awesome-icon  icon="chevron-up" /></span> </th></th>
              <th @click="sortBy('watched')"  :style="{ 'cursor': 'pointer' }"  scope="col">Watched? <span v-if="sortOrder === 'asc' && sortKey === 'watched'"> <font-awesome-icon  icon="chevron-down" /></span> <span v-if="sortOrder === 'desc' && sortKey === 'watched'"> <font-awesome-icon  icon="chevron-up" /></span> </th></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(show, index) in showsSorted" :key="index">
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
              </td>
            </tr>
          </tbody>
        </table>
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
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-year-group"
                      label="Year:"
                      label-for="form-year-input">
            <b-form-input id="form-year-input"
                          type="text"
                          v-model="addShowForm.year"
                          required
                          placeholder="Enter year">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-watched-group">
          <b-form-checkbox-group v-model="addShowForm.watched" id="form-checks">
            <b-form-checkbox value="true">Watched?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
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
                          v-model="editForm.year"
                          required
                          placeholder="Enter year">
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
import _ from 'lodash';

export default {
  data() {
    return {
      shows: [],
      sortKey: 'title',
      sortOrder: 'asc',
      addShowForm: {
        title: '',
        year: '',
        watched: [],
      },
      editForm: {
        id: '',
        title: '',
        year: '',
        watched: [],
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  computed: {
    showsSorted: function() {
      console.log(this.sortKey)
        return _.orderBy(this.shows, this.sortKey, this.sortOrder);
    },
},

  methods: {

 sortBy: function(key) {
        if (key == this.sortKey) {
            this.sortOrder = (this.sortOrder == 'asc') ? 'desc' : 'asc';
        } else {
            this.sortKey = key;
            this.sortOrder = 'asc';
        }
   },

    getShows() {
      const path = 'http://localhost:5000/shows';
      axios.get(path)
        .then((res) => {
          this.shows = res.data.shows;
          console.log(this.shows)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addShow(payload) {
      const path = 'http://localhost:5000/shows';
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
      const path = `http://localhost:5000/shows/${showID}`;
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
      const path = `http://localhost:5000/shows/${showID}`;
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
    initForm() {
      this.addShowForm.title = '';
      this.addShowForm.year = '';
      this.addShowForm.watched = [];
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.year = '';
      this.editForm.watched = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addShowModal.hide();
      let watched = false;
      if (this.addShowForm.watched[0]) watched = true;
      const payload = {
        title: this.addShowForm.title,
        year: this.addShowForm.year,
        watched, // property shorthand
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
    editShow(show) {
      this.editForm = show;
    },
  },
  created() {
    this.getShows();
  },
};
</script>
