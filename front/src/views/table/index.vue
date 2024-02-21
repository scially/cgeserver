<template>
  <div class="app-container">
    <el-button @click="handleSSRUpdateDialog(null)">添加</el-button>
    <el-dialog title="推流实例" :visible.sync="dialogVisible" width="40%">
      <el-form ref="form" :model="updateOrAddSSRForm" label-width="80px">
        <input v-model="updateOrAddSSRForm.uid" hidden type="text">
        <el-form-item label="推流名称">
          <el-input v-model="updateOrAddSSRForm.name" />
        </el-form-item>
        <el-form-item label="前端路径">
          <el-input v-model="updateOrAddSSRForm.frontpath" />
        </el-form-item>
        <el-form-item label="UE路径">
          <el-input v-model="updateOrAddSSRForm.uepath" placeholder="E:/Project/cgeservertest/Windows/cgeservertest/Binaries/Win64/cgeservertest.exe" />
        </el-form-item>
        <el-form-item label="分辨率">
          <div>
            <el-input v-model="updateOrAddSSRForm.xresolution" type="number">
              <template slot="prepend">X</template>
            </el-input>
            <el-input v-model="updateOrAddSSRForm.yresolution" type="number">
              <template slot="prepend">Y</template>
            </el-input>
          </div>
        </el-form-item>
        <el-form-item label="后台运行">
          <el-checkbox v-model="updateOrAddSSRForm.background" />
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSSRUpdateOrAdd()">确 定</el-button>
      </span>
    </el-dialog>
    <el-table v-loading="listLoading" :data="list" element-loading-text="Loading" border fit highlight-current-row>
      <el-table-column align="center" label="序号" width="80">
        <template slot-scope="scope">
          {{ scope.$index + 1 }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="推流名称">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column label="后台运行" align="center" width="90">
        <template slot-scope="scope">
          <el-checkbox :value="scope.row.background" />
        </template>
      </el-table-column>
      <el-table-column align="center" label="推流分辨率">
        <template slot-scope="scope">
          <span>{{ scope.row.xresolution }} x {{ scope.row.yresolution }}</span>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="推流状态" align="center">
        <template slot-scope="scope">
          <el-switch :value="scope.row.status" active-color="#13ce66" inactive-color="#ff4949" />
        </template>
      </el-table-column>
      <el-table-column label="推流详情" align="center" width="500">
        <template slot-scope="scope">
          <el-popover placement="right" title="详情" width="600" trigger="click">
            <p>推流地址: {{ baseUrl.replace('http', 'ws') }}/ws/streaming/server/{{ scope.row.uid }}</p>
            <p>拉染地址: {{ baseUrl.replace('http', 'ws') }}/ws/streaming/client/{{ scope.row.uid }}</p>
            <p>渲染地址: {{ baseUrl }}/static/{{ scope.row.uid }}/index.html?data={{ currentTime }}</p>
            <p>信令地址: {{ baseUrl.replace('http', 'ws') }}/ws/streaming/signal/{{ scope.row.uid }}</p>
            <p>UE路径: {{ scope.row.uepath }}</p>
            <p>前端路径: {{ scope.row.frontpath }}</p>
            <el-button slot="reference" size="mini">推流详情</el-button>
          </el-popover>
          <el-button size="mini" :disabled="scope.row.status" @click="handleSSRStart(scope.$index)">开始推流</el-button>
          <el-button size="mini" :disabled="!scope.row.status" @click="handleSSRStop(scope.$index)">停止推流</el-button>
          <el-button size="mini" @click="handleSSRNavigate(scope.row)">跳转</el-button>
          <el-button size="mini" @click="handleSSRUpdateDialog(scope.row)">编辑</el-button>

          <el-button size="mini" type="danger" @click="handleSSRDelete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { list, remove, add, query, update, start, stop } from '@/api/table'
import { info } from '@/api/dev'
import { Message } from 'element-ui'

let signalWebSocket = null

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: [],
      // ssr list loading
      listLoading: true,
      // ssr instance add or update
      dialogVisible: false,
      updateOrAddSSRForm: {
        uid: '',
        name: '',
        frontpath: '',
        uepath: '',
        xresolution: 1920,
        yresolution: 1080,
        background: true
      },
      // ssr frontpath refresh
      currentTime: Date.now()
    }
  },
  asyncComputed: {
    async baseUrl() {
      const response = await info()
      return `${response.data.protocol}://${response.data.host}:${response.data.port}`
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      list().then(response => {
        this.list.splice(0)
        response.data.forEach(element => {
          query({ 'uid': element.uid }).then(response => {
            element['status'] = response.data
            if (element['status']) {
              signalWebSocket = new WebSocket(`${this.baseUrl.replace('http', 'ws')}/ws/streaming/signal/${element.uid}`)
              signalWebSocket.onmessage = this.handleSignalMessage
            }
            this.list.push(element)
          })
        })
        this.listLoading = false
      })
    },
    handleSSRDelete(ind, ssr) {
      this.currentTime = Date.now()
      const uid = ssr.uid
      remove({ 'uid': uid }).then(response => {
        const ind = this.list.findIndex(e => e.uid === uid)
        this.list.splice(ind, 1)
      })
    },
    handleSSRStart(ind) {
      this.currentTime = Date.now()
      start({ 'uid': this.list[ind].uid }).then(response => {
        if (response.status === 200 && response.data) {
          this.list[ind].status = true
          signalWebSocket = new WebSocket(`${this.baseUrl.replace('http', 'ws')}/ws/streaming/signal/${this.list[ind].uid}`)
          signalWebSocket.onmessage = this.handleSignalMessage
        } else {
          Message({
            message: response.msg || 'Error',
            type: 'error',
            duration: 5 * 1000
          })
        }
      })
    },
    handleSSRStop(ind) {
      this.currentTime = Date.now()
      stop({ 'uid': this.list[ind].uid }).then(response => {
        if (response.status === 200 && response.data) {
          this.list[ind].status = false
          signalWebSocket = null
        } else {
          Message({
            message: response.msg || 'Error',
            type: 'error',
            duration: 5 * 1000
          })
        }
      })
    },
    handleSSRNavigate(ssr) {
      window.open(`${this.baseUrl}/static/${ssr.uid}/index.html?data=${Date.now()}`)
    },

    handleSSRUpdateDialog(ssr) {
      this.updateOrAddSSRForm.uid = ssr ? ssr.uid : ''
      this.updateOrAddSSRForm.name = ssr ? ssr.name : ''
      this.updateOrAddSSRForm.frontpath = ssr ? ssr.frontpath : ''
      this.updateOrAddSSRForm.uepath = ssr ? ssr.uepath : ''
      this.updateOrAddSSRForm.xresolution = ssr ? ssr.xresolution : 1920
      this.updateOrAddSSRForm.yresolution = ssr ? ssr.yresolution : 1080
      this.updateOrAddSSRForm.background = ssr ? ssr.background : false

      if (ssr && ssr.status) {
        Message({
          message: '先停止推流',
          type: 'error',
          duration: 5 * 1000
        })
      } else {
        this.dialogVisible = true
      }
    },
    handleSSRUpdateOrAdd() {
      const ssr = {
        name: this.updateOrAddSSRForm.name,
        background: this.updateOrAddSSRForm.background,
        uepath: this.updateOrAddSSRForm.uepath,
        frontpath: this.updateOrAddSSRForm.frontpath,
        xresolution: this.updateOrAddSSRForm.xresolution,
        yresolution: this.updateOrAddSSRForm.yresolution
      }

      if (!this.updateOrAddSSRForm.uid) {
        // add ssr
        this.dialogVisible = false
        add(ssr).then(response => {
          this.list.push(response.data)
        })
      } else {
        ssr['uid'] = this.updateOrAddSSRForm.uid
        update(ssr).then(response => {
          if (response.status === 200) {
            this.list.forEach(element => {
              if (element.uid === ssr.uid) {
                element.name = ssr.name
                element.background = ssr.background
                element.uepath = ssr.uepath
                element.frontpath = ssr.frontpath
                element.xresolution = ssr.xresolution
                element.yresolution = ssr.yresolution
              }
            })
            this.dialogVisible = false
          } else {
            Message({
              message: '修改失败',
              type: 'error',
              duration: 5 * 1000
            })
          }
        })
      }
    },
    // signal websocket event
    handleSignalMessage(event) {
      console.log(event.data)
    }
  }
}
</script>
