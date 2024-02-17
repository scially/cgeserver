<template>
  <div class="app-container">
    <el-button @click="dialogVisible = true">添加</el-button>
    <el-dialog title="添加SSR" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
      <p>推流名称</p><el-input v-model="ssrName" placeholder="ssr-demo"></el-input>
      <p>前端路径</p><el-input v-model="ssrFrontPath" placeholder="d:/vueproject/"></el-input>
      <p>UE路径</p><el-input v-model="ssrUEPath" placeholder="d:/ueproject/content/win64/ue.exe"></el-input>
      <p>分辨率</p>
      <div>
        <el-input type="number" v-model="ssrXResolution">
          <template slot="prepend">X</template>
        </el-input>
        <el-input type="number" v-model="ssrYResolution">
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
      <el-table-column label="推流名称">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column label="后台运行" align="center">
        <template slot-scope="scope">
          <el-switch :value="scope.row.background" disabled active-color="#13ce66" inactive-color="#ff4949">
          </el-switch>
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
          <el-switch :value="scope.row.status" active-color="#13ce66" inactive-color="#ff4949">
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column label="推流详情" align="center">
        <template slot-scope="scope">
          <el-popover placement="right" title="详情" width="600" trigger="click">
            <p>推流地址: /streaming/server/{{ scope.row.uid }}</p>
            <p>拉染地址: /streaming/client/{{ scope.row.uid }}</p>
            <p>渲染地址: /static/{{ scope.row.uid }}/index.html</p>
            <p>信令地址: /message/{{ scope.row.uid }}</p>
            <p>UE路径: {{ scope.row.uepath }}</p>
            <p>前端路径: {{ scope.row.frontpath }}</p>
            <el-button size="mini" slot="reference">推流详情</el-button>
          </el-popover>
          <el-button size="mini" type="danger" @click="handleSSRDelete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { list, remove, add } from '@/api/table'

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
      dialogVisible: false,
      list: [],
      listLoading: true,
      // ssr instance add
      ssrName: '',
      ssrFrontPath: '',
      ssrUEPath: '',
      ssrXResolution: 1920,
      ssrYResolution: 1080,
      ssrBackgound: true
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      list().then(response => {
        this.list.length = 0
        response.data.forEach(element => {
          this.list.push(element)
        })
        this.listLoading = false
      })
    },
    handleSSRDelete(ind, ssr) {
      const uid = ssr.uid
      remove({ 'uid': uid }).then(response => {
        fetchData()
      })
    },
    handleSSRAdd() {
      const ssr = {
        name: this.ssrName,
        background: this.ssrBackgound,
        uepath: this.ssrUEPath,
        frontpath: this.ssrFrontPath,
        xresolution: this.ssrXResolution,
        yresolution: this.ssrYResolution,
      }

      this.dialogVisible = false
      add(ssr).then(response => {
        this.fetchData()
      })
    }
  }
}
</script>
