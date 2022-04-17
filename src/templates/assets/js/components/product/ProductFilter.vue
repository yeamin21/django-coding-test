<template>
  <form @submit.prevent method="get" class="card-header">
    <div class="form-row justify-content-between">
      <div class="col-md-2">
        <input
          type="text"
          name="title"
          v-model="title"
          placeholder="Product Title"
          class="form-control"
        />
      </div>
      <div class="col-md-2">
        <select name="variant" v-model="variant" id="" class="form-control">
          <option value="" disabled>----Select Variant----</option>
          <optgroup
            v-for="variant in variants"
            :key="variant.id"
            :label="variant.title"
          >
            <option
              v-for="(variant_option, index) in variant.productvariants"
              :key="index"
              :value="variant_option.variant_title"
            >
              {{ variant_option.variant_title }}
            </option>
          </optgroup>
        </select>
      </div>

      <div class="col-md-3">
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">Price Range</span>
          </div>
          <input
            type="text"
            name="price_from"
            v-model="price_from"
            aria-label="First name"
            placeholder="From"
            class="form-control"
          />
          <input
            type="text"
            name="price_to"
            v-model="price_to"
            aria-label="Last name"
            placeholder="To"
            class="form-control"
          />
        </div>
      </div>
      <div class="col-md-2">
        <input
          type="date"
          name="date"
          v-model="date"
          placeholder="Date"
          class="form-control"
        />
      </div>
      <div class="col-md-1">
        <button
          type="submit"
          @click="
            $emit('apply', {
              title,
              variant,
              price_from,
              price_to,
              date,
              variant,
            })
          "
          class="btn btn-primary float-right"
        >
          <i class="fa fa-search"></i>
        </button>
      </div>
    </div>
  </form>
</template>

<script>
import axios from "axios";
export default {
  emits: ["apply"],
  data() {
    return {
      title: "",
      variant: "",
      price_from: "",
      price_to: "",
      date: "",
      variants: [],
    };
  },
  created() {
    this.loadVariants();
  },
  methods: {
    loadVariants() {
      axios
        .get("/api/variants")
        .then((response) => {
          this.variants = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style></style>
