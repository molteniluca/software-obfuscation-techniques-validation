	.file	"sha.c"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4,,15
	.type	sha_transform, @function
sha_transform:
.LFB60:
	.cfi_startproc
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	xorl	%ecx, %ecx
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$680, %rsp
	.cfi_def_cfa_offset 736
	movq	56(%rdi), %rdx
	movq	%fs:40, %rax
	movq	%rax, 664(%rsp)
	xorl	%eax, %eax
	movq	%rdx, 16(%rsp)
	movq	64(%rdi), %rdx
	movq	%rdx, 24(%rsp)
	movq	72(%rdi), %rdx
	movq	%rdx, 32(%rsp)
	movq	80(%rdi), %rdx
	movq	%rdx, 40(%rsp)
	movq	88(%rdi), %rdx
	movq	%rdx, 48(%rsp)
	movq	96(%rdi), %rdx
	movq	%rdx, 56(%rsp)
	movq	104(%rdi), %rdx
	movq	%rdx, 64(%rsp)
	movq	112(%rdi), %rdx
	movq	%rdx, 72(%rsp)
	movq	120(%rdi), %rdx
	movq	%rdx, 80(%rsp)
	movq	128(%rdi), %rdx
	movq	%rdx, 88(%rsp)
	movq	136(%rdi), %rdx
	movq	%rdx, 96(%rsp)
	movq	144(%rdi), %rdx
	movq	%rdx, 104(%rsp)
	movq	152(%rdi), %rdx
	movq	176(%rdi), %rax
	movdqa	32(%rsp), %xmm4
	movq	%rdx, 112(%rsp)
	movq	160(%rdi), %rdx
	movq	%rax, 136(%rsp)
	movdqa	48(%rsp), %xmm3
	movq	%rdx, 120(%rsp)
	movq	168(%rdi), %rdx
	movdqa	64(%rsp), %xmm0
	movq	%rdx, 128(%rsp)
	leaq	144(%rsp), %rdx
	jmp	.L2
	.p2align 4,,10
	.p2align 3
.L9:
	movq	%rsi, %rdx
.L2:
	movdqa	-64(%rdx), %xmm5
	addl	$4, %ecx
	leaq	40(%rdx), %r10
	cmpl	$28, %ecx
	leaq	-48(%rdx), %r9
	leaq	-64(%rdx), %r8
	movdqu	-24(%rdx), %xmm1
	leaq	64(%rdx), %rsi
	pxor	%xmm5, %xmm1
	pxor	%xmm1, %xmm4
	pxor	-128(%rdx), %xmm4
	movaps	%xmm4, (%rdx)
	movdqa	-48(%rdx), %xmm4
	movdqu	-8(%rdx), %xmm2
	pxor	%xmm4, %xmm2
	pxor	%xmm2, %xmm3
	pxor	-112(%rdx), %xmm3
	movaps	%xmm3, 16(%rdx)
	movdqa	-32(%rdx), %xmm3
	movdqu	8(%rdx), %xmm2
	pxor	%xmm3, %xmm2
	pxor	%xmm2, %xmm0
	pxor	-96(%rdx), %xmm0
	movaps	%xmm0, 32(%rdx)
	movdqa	-16(%rdx), %xmm0
	movdqu	24(%rdx), %xmm1
	pxor	%xmm0, %xmm1
	pxor	-80(%rdx), %xmm1
	pxor	%xmm5, %xmm1
	movaps	%xmm1, 48(%rdx)
	jne	.L9
	xorl	%eax, %eax
	.p2align 4,,10
	.p2align 3
.L3:
	addl	$1, %ecx
	movdqu	(%r10,%rax), %xmm0
	pxor	(%rdx,%rax), %xmm0
	pxor	(%r9,%rax), %xmm0
	pxor	(%r8,%rax), %xmm0
	movaps	%xmm0, (%rsi,%rax)
	addq	$16, %rax
	cmpl	$32, %ecx
	jne	.L3
	movq	24(%rdi), %rax
	movq	(%rdi), %r15
	leaq	16(%rsp), %r9
	movq	8(%rdi), %r14
	movq	16(%rdi), %r13
	leaq	176(%rsp), %rcx
	movq	32(%rdi), %rbx
	movq	%rax, (%rsp)
	movq	%rax, %rdx
	movq	%r15, %rax
	movq	%r13, %r11
	movq	%r14, %rsi
	movq	%rbx, 8(%rsp)
	jmp	.L4
	.p2align 4,,10
	.p2align 3
.L10:
	movq	%r11, %rdx
	movq	%r8, %rax
	movq	%r10, %r11
.L4:
	movq	%rax, %rbp
	movq	%rax, %r8
	movq	%rsi, %r10
	shrq	$27, %r8
	salq	$5, %rbp
	salq	$30, %r10
	orq	%r8, %rbp
	movq	%r11, %r8
	addq	(%r9), %rbp
	xorq	%rdx, %r8
	addq	$8, %r9
	andq	%rsi, %r8
	shrq	$2, %rsi
	xorq	%rdx, %r8
	orq	%rsi, %r10
	movq	%rax, %rsi
	leaq	1518500249(%rbp,%r8), %r8
	addq	%rbx, %r8
	cmpq	%r9, %rcx
	movq	%rdx, %rbx
	jne	.L10
	leaq	336(%rsp), %rbp
	jmp	.L5
	.p2align 4,,10
	.p2align 3
.L11:
	movq	%r10, %r11
	movq	%r9, %r8
	movq	%rsi, %r10
.L5:
	movq	%r8, %r9
	movq	%r8, %rsi
	addq	$8, %rcx
	shrq	$27, %rsi
	salq	$5, %r9
	orq	%rsi, %r9
	movq	%rax, %rsi
	xorq	%r10, %rsi
	xorq	%r11, %rsi
	leaq	1859775393(%r9,%rsi), %r9
	addq	-8(%rcx), %r9
	movq	%rax, %rsi
	salq	$30, %rsi
	shrq	$2, %rax
	orq	%rax, %rsi
	movq	%r8, %rax
	addq	%rdx, %r9
	cmpq	%rbp, %rcx
	movq	%r11, %rdx
	jne	.L11
	leaq	496(%rsp), %rbx
	movl	$2400959708, %r12d
	jmp	.L6
	.p2align 4,,10
	.p2align 3
.L12:
	movq	%rsi, %r10
	movq	%rax, %r9
	movq	%rdx, %rsi
.L6:
	movq	%r9, %rdx
	movq	%r9, %rax
	movq	%rsi, %rcx
	salq	$5, %rdx
	shrq	$27, %rax
	orq	%r10, %rcx
	orq	%rdx, %rax
	addq	0(%rbp), %rax
	movq	%rsi, %rdx
	andq	%r8, %rcx
	andq	%r10, %rdx
	addq	$8, %rbp
	orq	%rdx, %rcx
	movq	%r8, %rdx
	shrq	$2, %r8
	salq	$30, %rdx
	addq	%r12, %rax
	orq	%r8, %rdx
	movq	%r9, %r8
	addq	%rcx, %rax
	addq	%r11, %rax
	cmpq	%rbx, %rbp
	movq	%r10, %r11
	jne	.L12
	leaq	656(%rsp), %r11
	movl	$3395469782, %ebp
	jmp	.L7
	.p2align 4,,10
	.p2align 3
.L13:
	movq	%rdx, %rsi
	movq	%rcx, %rax
	movq	%r8, %rdx
.L7:
	movq	%rax, %r12
	movq	%rax, %rcx
	movq	%r9, %r8
	shrq	$27, %rcx
	salq	$5, %r12
	salq	$30, %r8
	orq	%rcx, %r12
	movq	%r9, %rcx
	addq	$8, %rbx
	xorq	%rdx, %rcx
	shrq	$2, %r9
	xorq	%rsi, %rcx
	orq	%r9, %r8
	movq	%rax, %r9
	leaq	(%r12,%rcx), %rcx
	addq	%rbp, %rcx
	addq	-8(%rbx), %rcx
	addq	%r10, %rcx
	cmpq	%r11, %rbx
	movq	%rsi, %r10
	jne	.L13
	addq	(%rsp), %rdx
	addq	8(%rsp), %rsi
	addq	%r14, %rax
	addq	%r15, %rcx
	addq	%r13, %r8
	movq	%rax, 8(%rdi)
	movq	664(%rsp), %rax
	xorq	%fs:40, %rax
	movq	%rcx, (%rdi)
	movq	%r8, 16(%rdi)
	movq	%rdx, 24(%rdi)
	movq	%rsi, 32(%rdi)
	jne	.L17
	addq	$680, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
.L17:
	.cfi_restore_state
	call	__stack_chk_fail
	.cfi_endproc
.LFE60:
	.size	sha_transform, .-sha_transform
	.section	.text.unlikely
.LCOLDE0:
	.text
.LHOTE0:
	.section	.text.unlikely
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4,,15
	.globl	sha_init
	.type	sha_init, @function
sha_init:
.LFB62:
	.cfi_startproc
	movl	$4023233417, %eax
	movq	$1732584193, (%rdi)
	movq	$271733878, 24(%rdi)
	movq	%rax, 8(%rdi)
	movl	$2562383102, %eax
	movq	$0, 40(%rdi)
	movq	%rax, 16(%rdi)
	movl	$3285377520, %eax
	movq	$0, 48(%rdi)
	movq	%rax, 32(%rdi)
	ret
	.cfi_endproc
.LFE62:
	.size	sha_init, .-sha_init
	.section	.text.unlikely
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text.unlikely
.LCOLDB2:
	.text
.LHOTB2:
	.p2align 4,,15
	.globl	sha_update
	.type	sha_update, @function
sha_update:
.LFB63:
	.cfi_startproc
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	movslq	%edx, %rax
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	movq	%rsi, %rbp
	movq	%rdi, %rbx
	subq	$8, %rsp
	.cfi_def_cfa_offset 64
	movq	40(%rdi), %rcx
	leaq	(%rcx,%rax,8), %rsi
	cmpq	%rsi, %rcx
	ja	.L20
	movq	48(%rdi), %rcx
.L21:
	movq	%rsi, 40(%rbx)
	movq	%rax, %rsi
	leaq	56(%rbx), %r12
	shrq	$29, %rsi
	movq	%rbp, %r13
	addq	%rsi, %rcx
	cmpl	$63, %edx
	movq	%rcx, 48(%rbx)
	jle	.L23
	leal	-64(%rdx), %r14d
	movl	%r14d, %r15d
	shrl	$6, %r15d
	movl	%r15d, %r13d
	addq	$1, %r13
	salq	$6, %r13
	addq	%rbp, %r13
	.p2align 4,,10
	.p2align 3
.L24:
	movq	0(%rbp), %rax
	movq	%rbx, %rdi
	addq	$64, %rbp
	movq	%rax, (%r12)
	movq	-56(%rbp), %rax
	movq	%rax, 8(%r12)
	movq	-48(%rbp), %rax
	movq	%rax, 16(%r12)
	movq	-40(%rbp), %rax
	movq	%rax, 24(%r12)
	movq	-32(%rbp), %rax
	movq	%rax, 32(%r12)
	movq	-24(%rbp), %rax
	movq	%rax, 40(%r12)
	movq	-16(%rbp), %rax
	movq	%rax, 48(%r12)
	movq	-8(%rbp), %rax
	movq	%rax, 56(%r12)
	movzbl	56(%rbx), %eax
	movzbl	57(%rbx), %edx
	movzbl	58(%rbx), %ecx
	movzbl	59(%rbx), %esi
	movb	%al, 59(%rbx)
	movzbl	64(%rbx), %eax
	movb	%cl, 57(%rbx)
	movb	%dl, 58(%rbx)
	movzbl	66(%rbx), %ecx
	movzbl	65(%rbx), %edx
	movb	%sil, 56(%rbx)
	movzbl	67(%rbx), %esi
	movb	%al, 67(%rbx)
	movb	%cl, 65(%rbx)
	movb	%dl, 66(%rbx)
	movb	%sil, 64(%rbx)
	movzbl	72(%rbx), %eax
	movzbl	73(%rbx), %edx
	movzbl	74(%rbx), %ecx
	movzbl	75(%rbx), %esi
	movb	%al, 75(%rbx)
	movzbl	80(%rbx), %eax
	movb	%cl, 73(%rbx)
	movb	%dl, 74(%rbx)
	movzbl	82(%rbx), %ecx
	movzbl	81(%rbx), %edx
	movb	%sil, 72(%rbx)
	movzbl	83(%rbx), %esi
	movb	%al, 83(%rbx)
	movzbl	88(%rbx), %eax
	movb	%cl, 81(%rbx)
	movb	%dl, 82(%rbx)
	movzbl	90(%rbx), %ecx
	movzbl	89(%rbx), %edx
	movb	%sil, 80(%rbx)
	movzbl	91(%rbx), %esi
	movb	%al, 91(%rbx)
	movzbl	96(%rbx), %eax
	movb	%cl, 89(%rbx)
	movb	%dl, 90(%rbx)
	movzbl	98(%rbx), %ecx
	movzbl	97(%rbx), %edx
	movb	%sil, 88(%rbx)
	movzbl	99(%rbx), %esi
	movb	%al, 99(%rbx)
	movb	%cl, 97(%rbx)
	movb	%dl, 98(%rbx)
	movb	%sil, 96(%rbx)
	movzbl	104(%rbx), %eax
	movzbl	105(%rbx), %edx
	movzbl	106(%rbx), %ecx
	movzbl	107(%rbx), %esi
	movb	%al, 107(%rbx)
	movzbl	112(%rbx), %eax
	movb	%cl, 105(%rbx)
	movb	%dl, 106(%rbx)
	movzbl	114(%rbx), %ecx
	movzbl	113(%rbx), %edx
	movb	%sil, 104(%rbx)
	movzbl	115(%rbx), %esi
	movb	%al, 115(%rbx)
	movb	%cl, 113(%rbx)
	movb	%dl, 114(%rbx)
	movb	%sil, 112(%rbx)
	call	sha_transform
	cmpq	%r13, %rbp
	jne	.L24
	sall	$6, %r15d
	subl	%r15d, %r14d
	movslq	%r14d, %rax
.L23:
	cmpq	$8, %rax
	jnb	.L25
	testb	$4, %al
	jne	.L40
	testq	%rax, %rax
	je	.L19
	movzbl	0(%r13), %edx
	testb	$2, %al
	movb	%dl, (%r12)
	jne	.L41
.L19:
	addq	$8, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
	.p2align 4,,10
	.p2align 3
.L20:
	.cfi_restore_state
	movq	48(%rdi), %rdi
	leaq	1(%rdi), %rcx
	jmp	.L21
	.p2align 4,,10
	.p2align 3
.L25:
	movq	0(%r13), %rdx
	leaq	8(%r12), %rcx
	andq	$-8, %rcx
	movq	%rdx, (%r12)
	movq	-8(%r13,%rax), %rdx
	movq	%rdx, -8(%r12,%rax)
	subq	%rcx, %r12
	addq	%r12, %rax
	subq	%r12, %r13
	andq	$-8, %rax
	cmpq	$8, %rax
	jb	.L19
	andq	$-8, %rax
	xorl	%edx, %edx
.L29:
	movq	0(%r13,%rdx), %rsi
	movq	%rsi, (%rcx,%rdx)
	addq	$8, %rdx
	cmpq	%rax, %rdx
	jb	.L29
	jmp	.L19
.L40:
	movl	0(%r13), %edx
	movl	%edx, (%r12)
	movl	-4(%r13,%rax), %edx
	movl	%edx, -4(%r12,%rax)
	jmp	.L19
.L41:
	movzwl	-2(%r13,%rax), %edx
	movw	%dx, -2(%r12,%rax)
	jmp	.L19
	.cfi_endproc
.LFE63:
	.size	sha_update, .-sha_update
	.section	.text.unlikely
.LCOLDE2:
	.text
.LHOTE2:
	.section	.text.unlikely
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4,,15
	.globl	sha_final
	.type	sha_final, @function
sha_final:
.LFB64:
	.cfi_startproc
	pushq	%r13
	.cfi_def_cfa_offset 16
	.cfi_offset 13, -16
	pushq	%r12
	.cfi_def_cfa_offset 24
	.cfi_offset 12, -24
	leaq	56(%rdi), %r13
	pushq	%rbp
	.cfi_def_cfa_offset 32
	.cfi_offset 6, -32
	pushq	%rbx
	.cfi_def_cfa_offset 40
	.cfi_offset 3, -40
	movq	%rdi, %rbx
	subq	$8, %rsp
	.cfi_def_cfa_offset 48
	movq	40(%rdi), %rbp
	movq	48(%rdi), %r12
	movq	%rbp, %rdx
	shrq	$3, %rdx
	andl	$63, %edx
	leal	1(%rdx), %eax
	movslq	%edx, %rdx
	movb	$-128, 56(%rdi,%rdx)
	cmpl	$56, %eax
	jle	.L43
	movl	$64, %edx
	movslq	%eax, %rcx
	addq	%r13, %rcx
	subl	%eax, %edx
	je	.L45
	xorl	%eax, %eax
.L44:
	movl	%eax, %esi
	addl	$1, %eax
	cmpl	%edx, %eax
	movb	$0, (%rcx,%rsi)
	jb	.L44
.L45:
	movzbl	56(%rbx), %eax
	movzbl	57(%rbx), %edx
	movq	%rbx, %rdi
	movzbl	58(%rbx), %ecx
	movzbl	59(%rbx), %esi
	movb	%dl, 58(%rbx)
	movb	%al, 59(%rbx)
	movzbl	65(%rbx), %edx
	movzbl	64(%rbx), %eax
	movb	%sil, 56(%rbx)
	movb	%cl, 57(%rbx)
	movzbl	67(%rbx), %esi
	movzbl	66(%rbx), %ecx
	movb	%al, 67(%rbx)
	movb	%dl, 66(%rbx)
	movzbl	72(%rbx), %eax
	movzbl	73(%rbx), %edx
	movb	%sil, 64(%rbx)
	movb	%cl, 65(%rbx)
	movzbl	75(%rbx), %esi
	movzbl	74(%rbx), %ecx
	movb	%al, 75(%rbx)
	movb	%dl, 74(%rbx)
	movzbl	80(%rbx), %eax
	movzbl	81(%rbx), %edx
	movb	%sil, 72(%rbx)
	movb	%cl, 73(%rbx)
	movzbl	83(%rbx), %esi
	movzbl	82(%rbx), %ecx
	movb	%al, 83(%rbx)
	movb	%dl, 82(%rbx)
	movb	%sil, 80(%rbx)
	movb	%cl, 81(%rbx)
	movzbl	88(%rbx), %eax
	movzbl	89(%rbx), %edx
	movzbl	90(%rbx), %ecx
	movzbl	91(%rbx), %esi
	movb	%dl, 90(%rbx)
	movb	%al, 91(%rbx)
	movzbl	97(%rbx), %edx
	movzbl	96(%rbx), %eax
	movb	%sil, 88(%rbx)
	movb	%cl, 89(%rbx)
	movzbl	99(%rbx), %esi
	movzbl	98(%rbx), %ecx
	movb	%al, 99(%rbx)
	movb	%dl, 98(%rbx)
	movzbl	104(%rbx), %eax
	movzbl	105(%rbx), %edx
	movb	%sil, 96(%rbx)
	movb	%cl, 97(%rbx)
	movzbl	107(%rbx), %esi
	movzbl	106(%rbx), %ecx
	movb	%al, 107(%rbx)
	movb	%dl, 106(%rbx)
	movzbl	112(%rbx), %eax
	movzbl	113(%rbx), %edx
	movb	%sil, 104(%rbx)
	movb	%cl, 105(%rbx)
	movzbl	115(%rbx), %esi
	movzbl	114(%rbx), %ecx
	movb	%al, 115(%rbx)
	movb	%dl, 114(%rbx)
	movb	%cl, 113(%rbx)
	movb	%sil, 112(%rbx)
	call	sha_transform
	leaq	8(%r13), %rdi
	movq	%r13, %rax
	movq	$0, 56(%rbx)
	movq	$0, 48(%r13)
	andq	$-8, %rdi
	subq	%rdi, %rax
	leal	56(%rax), %ecx
	xorl	%eax, %eax
	shrl	$3, %ecx
	rep stosq
.L46:
	movzbl	56(%rbx), %eax
	movzbl	57(%rbx), %edx
	movq	%rbx, %rdi
	movzbl	58(%rbx), %ecx
	movzbl	59(%rbx), %esi
	movb	%dl, 58(%rbx)
	movb	%al, 59(%rbx)
	movzbl	65(%rbx), %edx
	movzbl	64(%rbx), %eax
	movb	%sil, 56(%rbx)
	movb	%cl, 57(%rbx)
	movzbl	67(%rbx), %esi
	movzbl	66(%rbx), %ecx
	movb	%al, 67(%rbx)
	movb	%dl, 66(%rbx)
	movzbl	72(%rbx), %eax
	movzbl	73(%rbx), %edx
	movb	%sil, 64(%rbx)
	movb	%cl, 65(%rbx)
	movzbl	75(%rbx), %esi
	movzbl	74(%rbx), %ecx
	movb	%al, 75(%rbx)
	movb	%dl, 74(%rbx)
	movzbl	80(%rbx), %eax
	movzbl	81(%rbx), %edx
	movb	%sil, 72(%rbx)
	movb	%cl, 73(%rbx)
	movzbl	83(%rbx), %esi
	movzbl	82(%rbx), %ecx
	movb	%al, 83(%rbx)
	movb	%dl, 82(%rbx)
	movb	%sil, 80(%rbx)
	movb	%cl, 81(%rbx)
	movzbl	88(%rbx), %eax
	movzbl	89(%rbx), %edx
	movzbl	90(%rbx), %ecx
	movzbl	91(%rbx), %esi
	movb	%dl, 90(%rbx)
	movb	%al, 91(%rbx)
	movzbl	97(%rbx), %edx
	movzbl	96(%rbx), %eax
	movb	%sil, 88(%rbx)
	movb	%cl, 89(%rbx)
	movzbl	99(%rbx), %esi
	movzbl	98(%rbx), %ecx
	movb	%al, 99(%rbx)
	movb	%dl, 98(%rbx)
	movzbl	104(%rbx), %eax
	movzbl	105(%rbx), %edx
	movb	%sil, 96(%rbx)
	movb	%cl, 97(%rbx)
	movzbl	107(%rbx), %esi
	movzbl	106(%rbx), %ecx
	movb	%al, 107(%rbx)
	movb	%dl, 106(%rbx)
	movzbl	112(%rbx), %eax
	movzbl	113(%rbx), %edx
	movb	%sil, 104(%rbx)
	movb	%cl, 105(%rbx)
	movzbl	115(%rbx), %esi
	movzbl	114(%rbx), %ecx
	movb	%al, 115(%rbx)
	movb	%dl, 114(%rbx)
	movb	%sil, 112(%rbx)
	movb	%cl, 113(%rbx)
	movq	%r12, 168(%rbx)
	movq	%rbp, 176(%rbx)
	addq	$8, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 40
	popq	%rbx
	.cfi_def_cfa_offset 32
	popq	%rbp
	.cfi_def_cfa_offset 24
	popq	%r12
	.cfi_def_cfa_offset 16
	popq	%r13
	.cfi_def_cfa_offset 8
	jmp	sha_transform
	.p2align 4,,10
	.p2align 3
.L43:
	.cfi_restore_state
	movl	$56, %edx
	subl	%eax, %edx
	cltq
	addq	%r13, %rax
	cmpl	$8, %edx
	jb	.L65
	movl	%edx, %ecx
	movq	$0, (%rax)
	movq	$0, -8(%rax,%rcx)
	leaq	8(%rax), %rcx
	andq	$-8, %rcx
	subq	%rcx, %rax
	addl	%edx, %eax
	andl	$-8, %eax
	cmpl	$8, %eax
	jb	.L46
	andl	$-8, %eax
	xorl	%edx, %edx
.L51:
	movl	%edx, %esi
	addl	$8, %edx
	cmpl	%eax, %edx
	movq	$0, (%rcx,%rsi)
	jb	.L51
	jmp	.L46
	.p2align 4,,10
	.p2align 3
.L65:
	testb	$4, %dl
	jne	.L66
	testl	%edx, %edx
	je	.L46
	testb	$2, %dl
	movb	$0, (%rax)
	je	.L46
	xorl	%ecx, %ecx
	movw	%cx, -2(%rax,%rdx)
	jmp	.L46
	.p2align 4,,10
	.p2align 3
.L66:
	movl	$0, (%rax)
	movl	$0, -4(%rax,%rdx)
	jmp	.L46
	.cfi_endproc
.LFE64:
	.size	sha_final, .-sha_final
	.section	.text.unlikely
.LCOLDE3:
	.text
.LHOTE3:
	.section	.text.unlikely
.LCOLDB4:
	.text
.LHOTB4:
	.p2align 4,,15
	.globl	sha_stream
	.type	sha_stream, @function
sha_stream:
.LFB65:
	.cfi_startproc
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	movq	%rsi, %rcx
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	movq	%rdi, %rbx
	subq	$8232, %rsp
	.cfi_def_cfa_offset 8288
	movq	$1732584193, (%rdi)
	movq	$271733878, 24(%rdi)
	movq	%fs:40, %rax
	movq	%rax, 8216(%rsp)
	xorl	%eax, %eax
	movl	$4023233417, %eax
	movq	%rsi, 8(%rsp)
	movq	$0, 40(%rdi)
	movq	%rax, 8(%rdi)
	movl	$2562383102, %eax
	movq	$0, 48(%rdi)
	movq	%rax, 16(%rdi)
	movl	$3285377520, %eax
	movq	%rax, 32(%rdi)
	.p2align 4,,10
	.p2align 3
.L68:
	leaq	16(%rsp), %rdi
	movl	$8192, %edx
	movl	$1, %esi
	call	fread
	testl	%eax, %eax
	jle	.L78
	movq	40(%rbx), %rcx
	movslq	%eax, %rdx
	leaq	(%rcx,%rdx,8), %rsi
	cmpq	%rsi, %rcx
	movq	48(%rbx), %rcx
	jbe	.L70
	addq	$1, %rcx
.L70:
	movq	%rsi, 40(%rbx)
	movq	%rdx, %rsi
	leaq	56(%rbx), %r15
	shrq	$29, %rsi
	leaq	16(%rsp), %r12
	addq	%rsi, %rcx
	cmpl	$63, %eax
	movq	%rcx, 48(%rbx)
	jle	.L72
	leal	-64(%rax), %r13d
	leaq	16(%rsp), %rax
	movl	%r13d, %r14d
	movq	%rax, %rbp
	shrl	$6, %r14d
	movl	%r14d, %r12d
	addq	$1, %r12
	salq	$6, %r12
	addq	%rax, %r12
	.p2align 4,,10
	.p2align 3
.L73:
	movq	0(%rbp), %rax
	addq	$64, %rbp
	movq	%rax, (%r15)
	movq	-56(%rbp), %rax
	movq	%rax, 8(%r15)
	movq	-48(%rbp), %rax
	movq	%rax, 16(%r15)
	movq	-40(%rbp), %rax
	movq	%rax, 24(%r15)
	movq	-32(%rbp), %rax
	movq	%rax, 32(%r15)
	movq	-24(%rbp), %rax
	movq	%rax, 40(%r15)
	movq	-16(%rbp), %rax
	movq	%rax, 48(%r15)
	movq	-8(%rbp), %rax
	movq	%rax, 56(%r15)
	movzbl	56(%rbx), %eax
	movzbl	57(%rbx), %edx
	movzbl	58(%rbx), %esi
	movzbl	59(%rbx), %edi
	movb	%al, 59(%rbx)
	movzbl	64(%rbx), %eax
	movb	%sil, 57(%rbx)
	movb	%dl, 58(%rbx)
	movzbl	66(%rbx), %esi
	movzbl	65(%rbx), %edx
	movb	%dil, 56(%rbx)
	movzbl	67(%rbx), %edi
	movb	%al, 67(%rbx)
	movb	%sil, 65(%rbx)
	movb	%dl, 66(%rbx)
	movb	%dil, 64(%rbx)
	movzbl	72(%rbx), %eax
	movzbl	73(%rbx), %edx
	movzbl	74(%rbx), %esi
	movzbl	75(%rbx), %edi
	movb	%al, 75(%rbx)
	movzbl	80(%rbx), %eax
	movb	%sil, 73(%rbx)
	movb	%dl, 74(%rbx)
	movzbl	82(%rbx), %esi
	movzbl	81(%rbx), %edx
	movb	%dil, 72(%rbx)
	movzbl	83(%rbx), %edi
	movb	%al, 83(%rbx)
	movzbl	88(%rbx), %eax
	movb	%sil, 81(%rbx)
	movb	%dl, 82(%rbx)
	movzbl	90(%rbx), %esi
	movzbl	89(%rbx), %edx
	movb	%dil, 80(%rbx)
	movzbl	91(%rbx), %edi
	movb	%al, 91(%rbx)
	movzbl	96(%rbx), %eax
	movb	%sil, 89(%rbx)
	movb	%dl, 90(%rbx)
	movzbl	98(%rbx), %esi
	movzbl	97(%rbx), %edx
	movb	%dil, 88(%rbx)
	movzbl	99(%rbx), %edi
	movb	%al, 99(%rbx)
	movb	%sil, 97(%rbx)
	movb	%dl, 98(%rbx)
	movb	%dil, 96(%rbx)
	movzbl	104(%rbx), %eax
	movzbl	105(%rbx), %edx
	movzbl	106(%rbx), %esi
	movzbl	107(%rbx), %edi
	movb	%al, 107(%rbx)
	movzbl	112(%rbx), %eax
	movb	%sil, 105(%rbx)
	movb	%dl, 106(%rbx)
	movzbl	114(%rbx), %esi
	movzbl	113(%rbx), %edx
	movb	%dil, 104(%rbx)
	movzbl	115(%rbx), %edi
	movb	%al, 115(%rbx)
	movb	%sil, 113(%rbx)
	movb	%dl, 114(%rbx)
	movb	%dil, 112(%rbx)
	movq	%rbx, %rdi
	call	sha_transform
	cmpq	%r12, %rbp
	jne	.L73
	sall	$6, %r14d
	subl	%r14d, %r13d
	movslq	%r13d, %rdx
.L72:
	movq	%r12, %rsi
	movq	%r15, %rdi
	call	memcpy
	movq	8(%rsp), %rcx
	jmp	.L68
.L78:
	movq	%rbx, %rdi
	call	sha_final
	movq	8216(%rsp), %rax
	xorq	%fs:40, %rax
	jne	.L79
	addq	$8232, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
.L79:
	.cfi_restore_state
	call	__stack_chk_fail
	.cfi_endproc
.LFE65:
	.size	sha_stream, .-sha_stream
	.section	.text.unlikely
.LCOLDE4:
	.text
.LHOTE4:
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align 8
.LC5:
	.string	"%08lx %08lx %08lx %08lx %08lx\n"
	.section	.text.unlikely
.LCOLDB6:
	.text
.LHOTB6:
	.p2align 4,,15
	.globl	sha_print
	.type	sha_print, @function
sha_print:
.LFB66:
	.cfi_startproc
	subq	$16, %rsp
	.cfi_def_cfa_offset 24
	movq	8(%rdi), %rcx
	pushq	32(%rdi)
	.cfi_def_cfa_offset 32
	movq	24(%rdi), %r9
	movq	16(%rdi), %r8
	movl	$.LC5, %esi
	movq	(%rdi), %rdx
	xorl	%eax, %eax
	movl	$1, %edi
	call	__printf_chk
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE66:
	.size	sha_print, .-sha_print
	.section	.text.unlikely
.LCOLDE6:
	.text
.LHOTE6:
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
