<template>
    <div ref="player" class="app-container">
        <el-button type="primary" @click="linkStramingServer(url)">开始直播</el-button>
        <video ref="video" is="peer-stream" muted onplaying="getStats()" class="video-player">
            <track default kind="captions" srclang="en" />
        </video>
    </div>
</template>

<script>
import { info } from '@/api/dev'
import { Message } from 'element-ui'

export default {
    name: 'openstreaming',
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
                duration: 5 * 1000
            })
        } else {     
            const response = await info();
            const baseUrl = `${response.data.protocol}://${response.data.host}:${response.data.port}`
            this.url = `${baseUrl.replace('http', 'ws')}/ws/streaming/client/${this.uid}`
            
        }
    },
    methods: {
        async linkStramingServer(url) {
            document.getElementById('video').id = url
            document.getElementById('video').play();
      }
    }
}
</script>

<style>
.video-player{
    width: 1920px;
    height: 100%;
}
</style>
