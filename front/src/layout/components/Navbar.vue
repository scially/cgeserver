<template>
  <div class="navbar">
    <hamburger :is-active="sidebar.opened" class="hamburger-container" @toggleClick="toggleSideBar" />

    <breadcrumb class="breadcrumb-container" />

    <div class="right-menu">
      <el-dropdown class="avatar-container" trigger="click">
        <div class="avatar-wrapper">
          <img src="data:image/png;base64,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" class="user-avatar">
          <i class="el-icon-caret-bottom" />
        </div>
        <el-dropdown-menu slot="dropdown" class="user-dropdown">
          <router-link to="/">
            <el-dropdown-item>
              首页
            </el-dropdown-item>
          </router-link>
          <a target="_blank" href="https://github.com/scially/cgeserver/">
            <el-dropdown-item>Source Code</el-dropdown-item>
          </a>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Breadcrumb from '@/components/Breadcrumb'
import Hamburger from '@/components/Hamburger'

export default {
  components: {
    Breadcrumb,
    Hamburger
  },
  computed: {
    ...mapGetters([
      'sidebar'
    ])
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch('app/toggleSideBar')
    },
    async logout() {
      await this.$store.dispatch('user/logout')
      this.$router.push(`/login?redirect=${this.$route.fullPath}`)
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);

  .hamburger-container {
    line-height: 46px;
    height: 100%;
    float: left;
    cursor: pointer;
    transition: background .3s;
    -webkit-tap-highlight-color:transparent;

    &:hover {
      background: rgba(0, 0, 0, .025)
    }
  }

  .breadcrumb-container {
    float: left;
  }

  .right-menu {
    float: right;
    height: 100%;
    line-height: 50px;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 8px;
      height: 100%;
      font-size: 18px;
      color: #5a5e66;
      vertical-align: text-bottom;

      &.hover-effect {
        cursor: pointer;
        transition: background .3s;

        &:hover {
          background: rgba(0, 0, 0, .025)
        }
      }
    }

    .avatar-container {
      margin-right: 30px;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;

        .user-avatar {
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 25px;
          font-size: 12px;
        }
      }
    }
  }
}
</style>
