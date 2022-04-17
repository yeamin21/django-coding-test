<template>
  <section>
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="h3 mb-0 text-gray-800">Products</h1>
    </div>

    <div class="card">
      <product-filter @apply="applyFilter"></product-filter>
      <div class="card-body">
        <div class="table-response">
          <table class="table">
            <thead>
              <tr>
                <th>#</th>
                <th>Title</th>
                <th>Description</th>
                <th>Variant</th>
                <th width="150px">Action</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="product in products" :key="product.id">
                <td>{{ product.id }}</td>
                <td>
                  {{ product.title }}
                  <br />
                  Created at :
                  {{
                    Math.floor(
                      (new Date(
                        new Date().getTime() -
                          new Date(product.created_at).getTime()
                      ) %
                        31536000) /
                        86400
                    ) + " days ago"
                  }}
                </td>
                <td>{{ product.description }}</td>

                <td>
                  <dl
                    v-for="(
                      product_variant_price, index
                    ) in product.productvariantprice_set"
                    :key="index"
                    class="row mb-0"
                    style="height: 80px; overflow: hidden"
                    id="variant"
                  >
                    <dt class="col-sm-3 pb-0">
                      <span v-if="product_variant_price.product_variant_one">
                        {{
                          product_variant_price.product_variant_one
                            .variant_title
                        }}</span
                      >/
                      <span v-if="product_variant_price.product_variant_two">{{
                        product_variant_price.product_variant_two.variant_title
                      }}</span
                      >/
                      <span v-if="product_variant_price.product_variant_three">
                        {{
                          product_variant_price.product_variant_three
                            .variant_title
                        }}</span
                      >
                    </dt>
                    <dd class="col-sm-9">
                      <dl class="row mb-0">
                        <dd class="col-sm-4 pb-0">
                          Price : {{ product_variant_price.price }}
                        </dd>
                        <dd class="col-sm-8 pb-0">
                          InStock : {{ product_variant_price.stock }}.
                        </dd>
                      </dl>
                    </dd>
                  </dl>
                  <button
                    onclick="$('#variant').toggleClass('h-auto')"
                    class="btn btn-sm btn-link"
                  >
                    Show more
                  </button>
                </td>
                <td>
                  <div class="btn-group btn-group-sm">
                    <a
                      :href="`/product/${product.id}/update/`"
                      class="btn btn-success"
                      >Edit</a
                    >
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="card-footer">
        <div class="row justify-content-between">
          <div class="col-md-6">
            <p>
              Showing {{ pagination.start_index }} to
              {{ pagination.end_index }} out of {{ pagination.total_objects }}
            </p>
          </div>
          <div class="col-md-2">
            <div class="pagination">
              <span class="step-links">
                <button @click="loadPrev">&lt;</button>

                <button
                  v-for="(page, index) in pagination.total_pages"
                  :key="index"
                  :class="
                    page == pagination.current_page_number ? 'active' : ''
                  "
                  @click="setPage(page)"
                >
                  {{ page }}
                </button>
                <button @click="loadNext">&gt;</button>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";
import ProductFilter from "./ProductFilter.vue";

export default {
  components: { ProductFilter },
  data() {
    return {
      pagination: {
        current_page_number: 1,
      },
      products: [],
      total: 0,
    };
  },
  created() {
    this.getProducts();
  },
  methods: {
    applyFilter(values) {
      console.log(values);
      this.getProducts(values);
    },
    loadNext() {
      this.pagination.current_page_number++;
      this.getProducts({ page: this.pagination.current_page_number });
    },
    loadPrev() {
      this.pagination.current_page_number--;
      this.getProducts({ page: this.pagination.current_page_number });
    },
    setPage(page) {
      this.pagination.current_page_number = page;
      this.getProducts({ page: this.pagination.current_page_number });
    },
    loadFirst() {
      this.pagination.current_page_number = 1;
      this.getProducts({ page: this.pagination.current_page_number });
    },
    getProducts(params = {}) {
      axios.get("/api/products", { params: params }).then((response) => {
        const {
          page_size,
          start_index,
          end_index,
          total_objects,
          total_pages,
          current_page_number,
          next,
          previous,
        } = response.data;
        this.pagination = {
          start_index,
          end_index,
          page_size,
          total_objects,
          total_pages,
          current_page_number,
          next,
          previous,
        };
        this.products = response.data.results;
      });
    },
  },
};
</script>

<style scoped>
button {
  padding: 6px;
  background-color: aliceblue;
  border: 0;
}
.active {
  background: #0fc598;
}
</style>
