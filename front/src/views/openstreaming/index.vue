<template>
    <div id="playerUI">
      <div id="player"></div>
      <div id="overlay" class="overlay">
        <div>
          <div id="qualityStatus" class="greyStatus">●</div>
          <div id="overlayButton">+</div>
        </div>
        <div id="overlaySettings">
          <div id="KickOthers">
            <div class="settings-text">Kick all other players</div>
            <label class="btn-overlay">
              <input
                type="button"
                id="kick-other-players-button"
                class="overlay-button btn-flat"
                value="Kick"
              />
            </label>
          </div>
          <div id="FillWindow">
            <div class="settings-text">Enlarge Display to Fill Window</div>
            <label class="tgl-switch">
              <input
                type="checkbox"
                id="enlarge-display-to-fill-window-tgl"
                class="tgl tgl-flat"
                checked
              />
              <div class="tgl-slider"></div>
            </label>
          </div>
          <div id="QualityControlOwnership">
            <div class="settings-text">Quality control ownership</div>
            <label class="tgl-switch">
              <input
                type="checkbox"
                id="quality-control-ownership-tgl"
                class="tgl tgl-flat"
              />
              <div class="tgl-slider"></div>
            </label>
          </div>
          <div id="statsSetting">
            <div class="settings-text">Show Stats</div>
            <label class="tgl-switch">
              <input type="checkbox" id="show-stats-tgl" class="tgl tgl-flat" checked />
              <div class="tgl-slider"></div>
            </label>
            <div id="statsContainer">
              <div id="stats"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

<script>
import './player.css'

import { info } from '@/api/dev'
import { Message } from 'element-ui'

export default {
    name: 'openstreaming',
    data() {
        return {
            webRtcWidthValue: 1920,
            webRtcWeightValue: 1080,
        }
    },
    computed: {
        uid() {
            return this.$route.query.uid
        }
    },
    async mounted() {
        if (!this.uid) {
            Message({
                message: '先选择推流实例',
                type: 'error',
                duration: 3 * 1000
            })
        } else {     
            const response = await info();
            const baseUrl = `${response.data.protocol}://${response.data.host}:${response.data.port}`
            const url = `${baseUrl.replace('http', 'ws')}/ws/streaming/client/${this.uid}`

            this.ueload(url)
        }
    },
    methods: {
        ueload(url) {
            setupHtmlEvents()
            setupFreezeFrameOverlay()
            registerKeyboardEvents()
            start(url)
        }
    }
}
</script>

<style>
.video-player{
    width: 1920px;
    height: 1080px;
}
</style>
