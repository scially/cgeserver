<template>
  <div class="app-container">
    <el-button @click="dialogVisible = true">添加</el-button>
    <el-dialog title="添加SSR" :visible.sync="dialogVisible" width="30%">
      <p>推流名称</p><el-input v-model="ssrName" placeholder="ssr-demo" />
      <p>前端路径</p><el-input v-model="ssrFrontPath" placeholder="d:/vueproject/" />
      <p>UE路径</p><el-input v-model="ssrUEPath" placeholder="d:/ueproject/content/win64/ue.exe" />
      <p>分辨率</p>
      <div>
        <el-input v-model="ssrXResolution" type="number">
          <template slot="prepend">X</template>
        </el-input>
        <el-input v-model="ssrYResolution" type="number">
          <template slot="prepend">Y</template>
        </el-input>
      </div>
      <el-checkbox v-model="ssrBackgound">后台运行</el-checkbox>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSSRAdd()">确 定</el-button>
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
      <!-- <el-table-column label="推流路径" align="center">
        <template slot-scope="scope">
          {{ scope.row.uepath }}
        </template>
      </el-table-column> -->
      <!-- <el-table-column class-name="status-col" label="前端路径" align="center">
        <template slot-scope="scope">
          {{ scope.row.frontpath }}
        </template>
      </el-table-column> -->
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
      <el-table-column label="推流详情" align="center">
        <template slot-scope="scope">
          <el-popover placement="right" title="详情" width="600" trigger="click">
            <p>推流地址: {{ baseUrl }}/streaming/server/{{ scope.row.uid }}</p>
            <p>拉染地址: {{ baseUrl }}/streaming/client/{{ scope.row.uid }}</p>
            <p>渲染地址: {{ baseUrl }}/static/{{ scope.row.uid }}/index.html?data={{ currentTime }}</p>
            <p>信令地址: {{ baseUrl }}/message/{{ scope.row.uid }}</p>
            <p>UE路径: {{ scope.row.uepath }}</p>
            <p>前端路径: {{ scope.row.frontpath }}</p>
            <el-button slot="reference" size="mini">推流详情</el-button>
          </el-popover>
          <el-button size="mini" :disabled="scope.row.status" @click="handleSSRStart(scope.$index)">开始推流</el-button>
          <el-button size="mini" :disabled="!scope.row.status" @click="handleSSRStop(scope.$index)">停止推流</el-button>
          <el-button size="mini" type="danger" @click="handleSSRDelete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { list, remove, add, query, start, stop } from '@/api/table'
import { Message } from 'element-ui'

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
      baseUrl: process.env.VUE_APP_BASE_API,

      dialogVisible: false,
      list: [],
      // ssr list loading
      listLoading: true,
      // ssr instance add
      ssrName: '',
      ssrFrontPath: '',
      ssrUEPath: '',
      ssrXResolution: 1920,
      ssrYResolution: 1080,
      ssrBackgound: true,

      // ssr frontpath refresh
      currentTime: Date.now()
    }
  },
  created() {
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
    handleSSRAdd() {
      const ssr = {
        name: this.ssrName,
        background: this.ssrBackgound,
        uepath: this.ssrUEPath,
        frontpath: this.ssrFrontPath,
        xresolution: this.ssrXResolution,
        yresolution: this.ssrYResolution
      }

      this.dialogVisible = false
      add(ssr).then(response => {
        this.list.push(response.data)
      })
    },
    handleSSRStart(ind) {
      this.currentTime = Date.now()
      start({ 'uid': this.list[ind].uid }).then(response => {
        if (response.status === 200 && response.data) {
          this.list[ind].status = true
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
        } else {
          Message({
            message: response.msg || 'Error',
            type: 'error',
            duration: 5 * 1000
          })
        }
      })
    }
  }
}
</script>
