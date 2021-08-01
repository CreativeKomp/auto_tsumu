import {app, Menu, BrowserWindow, ipcMain} from 'electron';

// セキュアな Electron の構成
// 参考: https://qiita.com/pochman/items/64b34e9827866664d436
let win:any
const createWindow = (): void => {
  // レンダープロセスとなる、ウィンドウオブジェクトを作成する。
  win = new BrowserWindow({
    width: 360,
    height: 365,
    frame: true,
    resizable: true,
    webPreferences: {
      // ローカルで完結するためtrueにする
      nodeIntegration: true,
      contextIsolation: false,
    },
  });
  // 読み込む index.html。
  // tsc でコンパイルするので、出力先の dist の相対パスで指定する。
  win.loadFile('./index.html');

  // 開発者ツールを起動する
  // win.webContents.openDevTools();
  win.setPosition(50, 50);
};

// メニューバー設定
menubarSetting();

// Electronの起動準備が終わったら、ウィンドウを作成する。
app.whenReady().then(createWindow);

// すべての ウィンドウ が閉じたときの処理
app.on('window-all-closed', () => {
  // macOS 以外では、メインプロセスを停止する
  // macOS では、ウインドウが閉じてもメインプロセスは停止せず
  // ドックから再度ウインドウが表示されるようにする。
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // macOS では、ウインドウが閉じてもメインプロセスは停止せず
  // ドックから再度ウインドウが表示されるようにする。
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

ipcMain.handle('push-start', (event, message) => {
  win.setIgnoreMouseEvents(true);
  return 'ok';
})

ipcMain.handle('pyEnd', (event, error) => {
  console.log(error);
  win.setIgnoreMouseEvents(false);
  return;
})

ipcMain.handle('logger', (event, str) => {
  console.log(str);
  return;
})

// メニューバーの設定
function menubarSetting(): void {
  const template = [

    {
      label: '識別設定',
      submenu: [
        {
          label: 'ツム発見設定',
          click() {}
        },
        {
          label: 'ファン設定',
          click() {}
        },
      ],
    },
  ];
  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}
  