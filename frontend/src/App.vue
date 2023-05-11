<template>
  <v-app id="inspire">
    <!--<HelloWorld msg="Welcome to Your Vue.jsX App"/>-->
    <v-layout>
      <v-app-bar color="#fff" density="compact">
        <v-app-bar-title>KRITIS Selektor</v-app-bar-title>
      </v-app-bar>
      <v-main>
        <v-progress-linear color="success" :model-value="progress" :height="5"></v-progress-linear>
        <v-container>
          <v-row class="d-flex flex-row-reverse">
            <v-sheet class="ma-2 pa-2">
              <img src="./assets/logos.png">
            </v-sheet>
          </v-row>
          <v-row>
            <v-alert icon="mdi-information-outline" class="ma-3 mt-0"
              text="Die einzelnen Datensätze wurden auf Grundlage der BSI-KritisV (Anhang 1-7) gebildet.">
            </v-alert>
          </v-row>
          <v-row>
            <v-col cols="12" sm="4">
              <v-card title="1. Wähle einen Sektor aus" class="pa-2">
                <template v-slot:text>
                  <v-list lines="one">
                    <v-list-item v-for="item in sectors" :title="item.t" @click="selectSector(item.k)">
                      <template v-slot:prepend>
                        <v-icon :icon="item.i"></v-icon>
                      </template>
                    </v-list-item>
                  </v-list>
                  <v-divider></v-divider>
                  <v-list lines="one">
                    <v-list-item v-for="item in [{t: 'Staat und Verwaltung', k: 'sv', i: 'mdi-home'}, {t: 'Medien und Kultur', k: 'mk', i: 'mdi-drama-masks'}]" :title="item.t"
                      @click="selectInfo(item.k)">
                      <template v-slot:prepend>
                        <v-icon :icon="item.i"></v-icon>
                      </template>
                    </v-list-item>
                  </v-list>
                  <v-list-item title="Siedlungsabfallentsorgung" @click="selectInfo('sae')">
                    <template v-slot:append>
                      <v-badge color="error" content="Neu" inline></v-badge>
                    </template>
                    <template v-slot:prepend>
                        <v-icon icon="mdi-trash-can-outline"></v-icon>
                      </template>
                  </v-list-item>
                </template>
              </v-card>
            </v-col>
            <v-col cols="12" sm="8" v-if="isSelectedInfo">
              <v-card title="Information" class="pa-2">
                <template v-slot:text v-if="isSelectedInfo == 'sae'">
                  Der neue KRITIS-Sektor wurde mit der Novellierung des IT-Sicherheitsgesetzes in §2 Abs. 10 Nr. 1 BSIG
                  hinzugefügt. Die aktuelle Fassung der BSI-Kritisverordnung (BSI-KritisV) enthält daher noch keine
                  Definition, welche Einrichtungen/Anlagen/Teilanlagen aufgrund ihrer Bedeutung als Kritische
                  Infrastrukturen gelten.
                  Bis Ende des ersten Halbjahrs 2023 soll ein entsprechender Referentenentwurf für eine
                  Änderungsverordnung zur Aufnahme des Sektors "Siedlungsabfallentsorgung" vorliegen.
                  <v-divider></v-divider>
                  <p>
                    Siehe <a
                      href="">https://www.bsi.bund.de/DE/Themen/KRITIS-und-regulierte-Unternehmen/Kritische-Infrastrukturen/Sektorspezifische-Infos-fuer-KRITIS-Betreiber/Siedlungsabfallentsorgung/siedlungsabfallentsorgung.html</a>
                    ,<a
                      href="">https://www.bsi.bund.de/DE/Themen/KRITIS-und-regulierte-Unternehmen/Kritische-Infrastrukturen/KRITIS-aktuell/KRITIS-Meldungen/221212-BSI-KritisV-Siedlungsabfallentsorgung.html?nn=1081378</a>
                  </p>
                </template>
                <template v-slot:text v-else>
                  Die Sektoren "Staat und Verwaltung" sowie "Medien und Kultur" unterliegen nicht der Regulierung durch
                  das BSIG, sondern sind Angelegenheit einer Bund-Länder-Vereinbarung.
                </template>
              </v-card>
            </v-col>
            <v-col cols="12" sm="4" v-if="isSelectedSector">
              <v-card title="2. Wähle einen Anlagetyp aus" class="pa-2">
                <template v-slot:text>
                  <v-list lines="one">
                    <v-list-item v-for="facility in selectedSector" :title="facility.category"
                      @click="selectFacility(facility.criteria, facility.treshold)"></v-list-item>
                  </v-list>
                </template>
              </v-card>
            </v-col>
            <v-col cols="12" sm="4">
              <v-card title="3. Kriterium/Schwellwert" class="pa-2" v-if="isSelectedFacility">
                <v-table>
                  <thead>
                    <tr>
                      <th>Kriterium</th>
                      <th>Schwellwert</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{{ selectedFacility.c }}</td>
                      <td>
                        <v-chip>{{ selectedFacility.t }}</v-chip>
                      </td>
                    </tr>
                  </tbody>
                </v-table>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </v-layout>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import json from './assets/results.json'
import { toRaw } from 'vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  },
  data() {
    return {
      sectors: [{ t: 'Energie', k: 'energy', i: 'mdi-wind-turbine'}, {t: 'Wasser', k: 'water', i: 'mdi-water'}, {t: 'Ernährung', k: 'food', i: 'mdi-food-apple-outline'}, {t: 'IT und ITK', k:'it', i: 'mdi-server'},{t:  'Gesundheit', k: 'health', i: 'mdi-heart-circle-outline'},{t: 'Finanz- und Versicherungswesen', k: 'finance', i: 'mdi-finance'}, {t: 'Transport und Verkehr', k: 'transport', i: 'mdi-train-car' }],
      kritisData: json,
      progress: 100 / 3,
      isSelectedSector: false,
      isSelectedFacility: false,
      isSelectedInfo: false,
      selectedSector: [],
      selectedFacility: {},
      active: ""
    }
  },
  methods: {
    selectSector(sector) {
      let data = toRaw(this.kritisData)[sector]
      this.selectedSector = data
      this.isSelectedSector = true
      this.isSelectedFacility = false
      this.isSelectedInfo = false
      this.progress = 50
    },
    selectInfo(infoKey) {
      this.isSelectedInfo = infoKey
      this.isSelectedSector = false
      this.isSelectedFacility = false
      this.progress = 100
    },
    selectFacility(criteria, treshold) {
      if (!this.isSelectedFacility) {
        this.isSelectedFacility = true
      }

      this.active = "v-list-item--active"
      this.progress = 100
      this.selectedFacility = { 'c': criteria, 't': treshold }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333;
}
</style>
