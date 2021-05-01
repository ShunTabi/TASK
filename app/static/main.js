"use strict";
//定義
function getTime() {
    const now = new Date(),
        y = now.getFullYear(),
        m = now.getMonth() + 1,
        d = now.getDate();
    const date = `${y}-${m}-${d}`;
    return date;
}
const LimBox = [5, 10, 20];
const msg = "成功しました"
function test1(tg) {
    // alert(tg);
    // console.log(tg);
}
function test2(tg) {
    alert(tg);
    console.log(tg);
}
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
//VueRouter
const router = new VueRouter({
    routes: [
        {
            path: "/task/:page",
            component: {
                template: "#task",
                delimiters: ["[[", "]]"],
                data: function () {
                    return {
                        box: [],
                        genreBox: [],
                        task: "",
                        prior: "選択してください",
                        genre: "選択してください",
                        data: "",
                        ONOFF: true,
                        Id: 0,
                        FORM: false,
                        limBox: LimBox,
                        lim: 10,//LimBox[1],
                        prior1: "ALL",
                        mx: 1,
                    }
                },
                methods: {
                    PP: function (tg) {
                        this.$router.push(`/task/${parseInt(this.$route.params.page) + tg}`);
                        this.axiosSELECT1();
                    },
                    axiosSELECT1: function () {
                        const params = new URLSearchParams();
                        params.append("method", "SELECT1");
                        params.append("lim", this.lim);
                        axios.post(`http://localhost:8000/app/task/${this.$route.params.page}`, params)
                            .then(res => {
                                this.box = res.data.box;
                                this.mx = Math.floor((res.data.mx - 1) / this.lim) + 1;
                            })
                            .catch(res => {
                                test1(res);
                            });
                    },
                    axiosSELECT2: function () {
                        const params = new URLSearchParams();
                        params.append("method", "SELECT2");
                        axios.post("http://localhost:8000/app/task/1", params)
                            .then(res => {
                                this.genreBox = res.data.box;
                                test1(res);
                            })
                            .catch(res => {
                                test1(res);
                            });
                    },
                    axiosSELECT3: function (tg) {
                        this.Id = tg;
                        const params = new URLSearchParams();
                        params.append("method", "SELECT3");
                        params.append("Id", tg);
                        axios.post("http://localhost:8000/app/task/1", params)
                            .then(res => {
                                this.task = res.data.box[0][0]
                                this.prior = res.data.box[0][1]
                                this.genre = res.data.box[0][2]
                                this.date = res.data.box[0][3]
                                this.ONOFF = false;
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    axiosINSERT: function () {
                        const params = new URLSearchParams()
                        params.append("task", this.task);
                        params.append("prior", this.prior);
                        params.append("genre", this.genre);
                        params.append("date", this.date);
                        params.append("method", "INSERT");
                        axios.post("http://localhost:8000/app/task/1", params)
                            .then(res => {
                                test1(res);
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    axiosUPDATE: function () {
                        const params = new URLSearchParams();
                        params.append("task", this.task);
                        params.append("prior", this.prior);
                        params.append("genre", this.genre);
                        params.append("date", this.date);
                        params.append("Id", this.Id);
                        params.append("method", "UPDATE");
                        axios.post("http://localhost:8000/app/task/1", params)
                            .then(res => {
                                test1(msg);
                                this.ONOFF = true;
                                this.task = "";
                                this.prior = "選択してください";
                                this.genre = "選択してください";
                                this.date = getTime();
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    axiosDELETE: function (tg) {
                        const params = new URLSearchParams();
                        params.append("method", "DELETE");
                        params.append("Id", tg);
                        axios.post("http://localhost:8000/app/task/1", params)
                            .then(res => {
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    FC: function () {
                        this.FORM = !this.FORM;
                    }
                },
                created: function () {
                    this.axiosSELECT1();
                    this.axiosSELECT2();
                    this.date = getTime();
                }
            }
        },
        {
            path: "/activity/:page",
            component: {
                template: "#activity1",
                delimiters: ["[[", "]]"],
                data: function () {
                    return {
                        taskBox: [],
                        task1: "選択してください",
                        today: "",
                        next: "",
                        date: "",
                        ONOFF: true,
                        taskBox: [],
                        activityBox: [],
                        task2: "ALL",
                        FORM: false,
                        limBox: LimBox,
                        lim: LimBox[0],
                        task2: "ALL",
                        mx: 1,
                    }
                },
                methods: {
                    PP: function (tg) {
                        this.$router.push(`/activity/${parseInt(this.$route.params.page) + tg}`);
                        this.axiosSELECT1();
                    },
                    axiosSELECT1: function () {
                        const params = new URLSearchParams();
                        params.append("method", "SELECT1");
                        params.append("lim", this.lim);
                        axios.post(`http://localhost:8000/app/activity/${this.task2}/${this.$route.params.page}`, params)
                            .then(res => {
                                this.activityBox = res.data.box;
                                this.mx = Math.floor((res.data.mx - 1) / this.lim) + 1;
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    axiosSELECT2: function () {
                        const params = new URLSearchParams();
                        params.append("method", "SELECT2");
                        axios.post(`http://localhost:8000/app/activity/${this.task2}/1`, params)
                            .then(res => {
                                this.taskBox = res.data.box;
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    axiosSELECT3: function (tg) {
                        this.Id = tg;
                        const params = new URLSearchParams();
                        params.append("method", "SELECT3");
                        axios.post(`http://localhost:8000/app/activity/SELECT/${tg}`, params)
                            .then(res => {
                                this.task1 = res.data.box[0][0]
                                this.today = res.data.box[0][1]
                                this.next = res.data.box[0][2]
                                this.date = res.data.box[0][3]
                                this.ONOFF = false
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    axiosINSERT: function () {
                        const params = new URLSearchParams();
                        params.append("method", "INSERT");
                        params.append("task", this.task1);
                        params.append("today", this.today);
                        params.append("next", this.next);
                        params.append("date", this.date);
                        axios.post("http://localhost:8000/app/activity/INSERT/1", params)
                            .then(res => {
                                test1(msg);
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    axiosUPDATE: function () {
                        const params = new URLSearchParams();
                        params.append("method", "UPDATE");
                        params.append("Id", this.Id);
                        params.append("task", this.task1);
                        params.append("today", this.today);
                        params.append("next", this.next);
                        params.append("date", this.date);
                        axios.post("http://localhost:8000/app/activity/UPDATE/1", params)
                            .then(res => {
                                test1(msg);
                                this.task1 = "選択してください";
                                this.today = "";
                                this.next = "";
                                this.date = getTime();
                                this.ONOFF = true;
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    axiosDELETE: function (tg) {
                        const params = new URLSearchParams();
                        params.append("method", "DELETE");
                        params.append("Id", tg);
                        axios.post("http://localhost:8000/app/activity/DELETE/1", params)
                            .then(res => {
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    FC: function () {
                        this.FORM = !this.FORM;
                    }
                },
                created: function () {
                    this.axiosSELECT1();
                    this.axiosSELECT2();
                    this.date = getTime();
                }
            },
        },
        {
            path: "/activity/:key/:page",
            component: {
                template: "#activity2",
                delimiters: ["[[", "]]"],
                data: function () {
                    return {
                        activityBox: [],
                        task: "",
                        today: "",
                        next: "",
                        date: "",
                        ONOFF: true,
                        FORM: false,
                        limBox: LimBox,
                        lim: LimBox[0],
                        mx: 1,
                    }
                },
                methods: {
                    PP: function (tg) {
                        this.$router.push(`/activity/${this.$route.params.key}/${parseInt(this.$route.params.page) + tg}`);
                        this.axiosSELECT1();
                    },
                    axiosSELECT1: function () {
                        const params = new URLSearchParams();
                        params.append("method", "SELECT1");
                        params.append("lim", this.lim);
                        axios.post(`http://localhost:8000/app/activity/${this.$route.params.key}/${this.$route.params.page}`, params)
                            .then(res => {
                                this.activityBox = res.data.box;
                                this.mx = Math.floor((res.data.mx - 1) / this.lim) + 1;
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    axiosSELECT3: function (tg) {
                        this.Id = tg;
                        const params = new URLSearchParams();
                        params.append("method", "SELECT3");
                        axios.post(`http://localhost:8000/app/activity/SELECT/${tg}`, params)
                            .then(res => {
                                this.task1 = res.data.box[0][0]
                                this.today = res.data.box[0][1]
                                this.next = res.data.box[0][2]
                                this.date = res.data.box[0][3]
                                this.ONOFF = false
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    axiosINSERT: function () {
                        const params = new URLSearchParams();
                        params.append("method", "INSERT");
                        params.append("task", this.task);
                        params.append("today", this.today);
                        params.append("next", this.next);
                        params.append("date", this.date);
                        axios.post("http://localhost:8000/app/activity/INSERT/1", params)
                            .then(res => {
                                test1(msg);
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    axiosUPDATE: function () {
                        const params = new URLSearchParams();
                        params.append("method", "UPDATE");
                        params.append("Id", this.Id);
                        params.append("task", this.task1);
                        params.append("today", this.today);
                        params.append("next", this.next);
                        params.append("date", this.date);
                        axios.post("http://localhost:8000/app/activity/UPDATE/1", params)
                            .then(res => {
                                test1(msg);
                                this.today = "";
                                this.next = "";
                                this.date = getTime();
                                this.ONOFF = true;
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    axiosDELETE: function (tg) {
                        const params = new URLSearchParams();
                        params.append("method", "DELETE");
                        params.append("Id", tg);
                        axios.post("http://localhost:8000/app/activity/DELETE/1", params)
                            .then(res => {
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    FC: function () {
                        this.FORM = !this.FORM;
                    }
                },
                created: function () {
                    this.task = this.$route.params.key;
                    this.axiosSELECT1();
                    this.date = getTime();
                }
            }
        },
        {
            path: "/classification/:page",
            component: {
                template: "#classification",
                delimiters: ["[[", "]]"],
                data: function () {
                    return {
                        date: "",
                        genre: "",
                        box: [],
                        ONOFF: true,
                        Id: 0,
                        FORM: false,
                        limBox: LimBox,
                        lim: LimBox[0],
                        mx: 1,
                    }
                },
                methods: {
                    PP: function (tg) {
                        this.$router.push(`/classification/${parseInt(this.$route.params.page) + tg}`);
                        this.axiosSELECT1();
                    },
                    axiosSELECT1: function () {
                        const params = new URLSearchParams();
                        params.append("method", "SELECT1");
                        params.append("lim", this.lim);
                        axios.post(`http://localhost:8000/app/classification/${this.$route.params.page}`, params)
                            .then(res => {
                                this.box = res.data.box;
                                this.mx = Math.floor((res.data.mx - 1) / this.lim) + 1;
                            })
                            .catch(res => {
                                test2(res);
                            });
                    },
                    axiosSELECT2: function (tg) {
                        this.Id = tg;
                        const params = new URLSearchParams();
                        params.append("Id", tg);
                        params.append("method", "SELECT2")
                        axios.post("http://localhost:8000/app/classification/1", params)
                            .then(res => {
                                this.ONOFF = false;
                                this.genre = res.data.box[0][0];
                                this.date = res.data.box[0][1];
                            })
                            .catch(function (error) { alert(error) });
                    },
                    axiosINSERT: function () {
                        const params = new URLSearchParams();
                        params.append("genre", this.genre);
                        params.append("date", this.date);
                        params.append("method", "INSERT");
                        axios.post("http://localhost:8000/app/classification/1", params)
                            .then(res => {
                                test1(msg);
                                this.axiosSELECT1();
                            })
                            .catch(function (error) {
                                test2(res);
                            });
                    },
                    axiosUPDATE: function () {
                        const params = new URLSearchParams();
                        params.append("Id", this.Id);
                        params.append("genre", this.genre);
                        params.append("date", this.date);
                        params.append("method", "UPDATE")
                        axios.post("http://localhost:8000/app/classification/1", params)
                            .then(res => {
                                test1(msg);
                                this.ONOFF = true;
                                this.Id = 0;
                                this.genre = "";
                                this.date = getTime();
                                this.axiosSELECT1();
                            })
                            .catch(function (error) { alert(error) });
                    },
                    axiosDELETE: function (tg) {
                        const params = new URLSearchParams();
                        params.append("method", "DELETE");
                        params.append("Id", tg);
                        axios.post("http://localhost:8000/app/classification/1", params)
                            .then(res => {
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                test2(res); F
                            });
                    },
                    FC: function () {
                        this.FORM = !this.FORM;
                    }
                },
                created: function () {
                    this.date = getTime();
                    this.axiosSELECT1();
                }
            }
        },
        {
            path: "/error",
            component: {
                template: "#error",
                delimiters: ["[[", "]]"],
                methods: {
                },
            }
        },
    ]
});

const app = new Vue({
    el: "#app",
    router: router,
    created: function () {
    }
});